from django.shortcuts import render, redirect
from django.conf import settings
from django.template import RequestContext
from cart.cart import Cart
from .models import OrderItem, Order, ShippingInformation, Payment
from users.models import Profile, User
from sell.models import Revenue
from sell.views import MONTHS
from .forms import OrderCreateForm, ShippingInformationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View
import stripe
from django.contrib import messages
from datetime import datetime
import decimal

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="/accounts/login")
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = ShippingInformationForm(request.POST)
        if form.is_valid():
            # first create an order
            order = Order.objects.create(
                paid=False,
                profile=request.user.profile
            )
            fullname = form.cleaned_data['fullname']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            street_address = form.cleaned_data['street_address']
            apartment = form.cleaned_data['apartment']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            # Now create new shipping information data
            shipping_address = ShippingInformation.objects.create(
                fullname=fullname,
                phone_number=phone_number,
                email=email,
                street_address=street_address,
                apartment=apartment,
                country=country,
                state=state,
                city=city,
                postal_code=postal_code,
                order=order,
                profile=request.user.profile
            )
            for item in cart:
                OrderItem.objects.create(order=order, seller=item['product'].seller, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
                order.seller.add(item['product'].seller)
            # clear the cart
            cart.clear()
            return redirect("order:payment", pk=order.pk)
    else:
        form = ShippingInformationForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_details.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        # Get the user profile
        self.object = self.get_object()
        profile = None
        try:
            profile = Profile.objects.get(user=self.request.user)
            # Check if the user is the owner of the order
            if profile.pk != self.object.profile.pk:
                return redirect("order:http-404-not-found")
        except Profile.DoesNotExist:
            # Other wise user needs to create a profile
            return redirect("users:create-profile")

        context = self.get_context_data(object=self.object)

        # Now check if a user had made any
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all()
        return context


# A 404 not found page
def http_404_not_found(request):
    response = render(request, 'order/404.html', {})
    response.status_code = 404
    return response


class PaymentView(View):
    def get(self, *args, **kwargs):
        order_id = int(kwargs['pk'])
        context = {}
        try:
            order = Order.objects.get(pk=order_id)
            context['order'] = order
        except Order.DoesNotExist:
            pass

        return render(self.request, "order/payment.html", context)

    def post(self, *args, **kwargs):
        order_id = int(kwargs['pk'])
        context = {}
        try:
            order = Order.objects.get(pk=order_id)
            # Token is created using Stripe Checkout or Elements!
            # Get the payment token ID submitted by the form:
            token = self.request.POST.get('stripeToken')
            amount = int(order.get_total_cost() * 100)

            try:
                # Use Stripe's library to make requests...
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description='Charge for ' + self.request.user.email,
                    source=token,
                )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = amount
                payment.save()

                # update the order
                order.paid = True
                order.payment = payment
                order.save()

                # get all the sellers associated with this order
                sellers = order.seller.all()

                # now give the sellers their money
                for seller in sellers:
                    # now filter order items according to seller
                    items = order.items.filter(seller=seller)
                    amount = 0
                    for item in items:
                        amount = amount + item.get_cost()
                        yebhonzo = 0
                        if item.price < 30:
                            yebhonzo = decimal.Decimal(
                                amount) * decimal.Decimal(0.1)
                        else:
                            yebhonzo = decimal.Decimal(
                                amount) * decimal.Decimal(0.3)
                        # Deduct the money that goes to achironet market place
                        amount = amount - yebhonzo

                    # now that we have calculated the amount given to the user
                    # now assign it to the recent Revenue object of that user
                    latest = None
                    try:
                        latest = seller.sales.latest('created')
                        latest_revenue_creation_date = latest.created
                        today = datetime.now()
                        # Now compare the two dates
                        if today.month > latest_revenue_creation_date.month and today.year == latest_revenue_creation_date.year:
                            if today.day > latest_revenue_creation_date.day:
                                # Then now create a new revenue data object
                                previous = latest
                                carried = 0
                                if previous.sales < 100:
                                    previous.paid = True
                                    carried = previous.sales
                                    previous.save()

                                latest = Revenue.objects.create(
                                    month=MONTHS[today.month],
                                    products_sold=0,
                                    sales=carried,
                                    seller=seller,
                                    year=str(today.year)
                                )

                        accumulated = latest.sales
                        accumulated = accumulated + (amount)

                        latest.sales = accumulated
                        latest.products_sold += items.count()
                        latest.save()
                    # Now the revenue object has not been created yet
                    # Because this is a still new operator
                    except Revenue.DoesNotExist:
                        today = datetime.now()
                        latest = Revenue.objects.create(
                            month=MONTHS[today.month],
                            products_sold=items.count(),
                            sales=amount,
                            seller=seller,
                            year=str(today.year)
                        )

                # Everything has gone well the transaction has finished
                messages.success(self.request, "Your order was successful")
                return render(self.request, 'order/created.html', {'order': order})
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body.get('error', {})
                messages.error(self.request, f"{err.get('message')}")
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.error(
                    self.request, "Payment not successful, rate limit error")
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.error(
                    self.request, "Payment not successful, invalid parameters.")
                print(e)

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.error(
                    self.request, "Payment not successful, authentication error")
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.error(
                    self.request, "Payment not successful, could not establish connection")
            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.error(
                    self.request, "Something went wrong you were not charged please try again")
                print(e)
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                # Send an email to ourselves
                messages.error(
                    self.request, "A serious error occured, we have been notified")
                print(e)

        except Order.DoesNotExist:
            messages.info(self.request, "Order does not exist")

        return redirect("shop:product_list")
