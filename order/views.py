from django.shortcuts import render, redirect
from django.template import RequestContext
from cart.cart import Cart
from .models import OrderItem, Order, ShippingInformation
from users.models import Profile, User
from .forms import OrderCreateForm, ShippingInformationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView


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
            return render(request, 'order/created.html', {'order': order})
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
