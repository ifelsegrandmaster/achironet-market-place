from django.shortcuts import render, redirect, reverse
from users.models import RequestReviewGroup, Testmonial, SellerProfile, Profile
from order.models import Order, OrderItem
from sell.models import Revenue
from shop.models import Product, OverView, Specification,Attribute, ProductImage
from .models import EmailNewsletter
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from decimal import Decimal, ROUND_UP
import re
from django.http import (
    HttpResponseForbidden,
    HttpResponseServerError,
    HttpResponseNotFound,
    JsonResponse
)
from .forms import (
    RequestReviewForm,
    ModerateTestmonialForm,
    EmailNewsletterForm,
    DeleteEmailNewsletterForm,
    OrderFilterForm,
    SellerFilterForm,
    CustomerFilterForm,
    ChangeItemForm,
    ChangeOrderForm,
    ProductFilterForm,
    RevenueFilterForm
)

from shop.forms import *
from datetime import datetime
import json
from django.core.mail import send_mail
# Create your views here.

# the home dashboard, person should be logged in to view this
# a person should be a super_user to view this
def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


@login_required(login_url="/accounts/login")
def dashboard(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")

    context = {
        "sellers_count": SellerProfile.objects.all().count(),
        "sellers": SellerProfile.objects.all().order_by('-created')[:5],
        "customers_count": Profile.objects.all().count(),
        "customers": Profile.objects.all().order_by('-pk')[:5],
        "orders_count": Order.objects.all().count(),
        "orders": Order.objects.all().order_by('-created')[:5],
    }
    return render(request, "achironet_admin/dashboard.html", context)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'achironet_admin/order_details.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all()
        return context


# ship an order
def ship_order(request):
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")

    if request.method == "POST":
        payload = {}
        try:
            data = json.loads(request.body)
            # check if the form is valid
            form = ChangeOrderForm(data)
            if form.is_valid():
                # process
                try:
                    order = Order.objects.get(pk=form.cleaned_data['order_id'])
                    if order.is_ready():
                        if order.shipped:
                            order.shipped = False
                            order.save()
                            payload['shipped'] = False
                        else:
                            order.shipped = True
                            order.save()
                            payload['shipped'] = True
                        payload['success'] = True
                        return JsonResponse(payload)
                    else:
                        return JsonResponse({
                            "success": False,
                            "message": "Cannot ship product",
                            "not_ready": True
                        })
                except Order.DoesNotExist:
                    return JsonResponse({
                        "success": False
                    })

        except json.JSONDecodeError:
            return JsonResponse({"success": False})
    return JsonResponse({"message": "Ooops nothing for you here."})


# List all the sellers who have registered
# person should be logged in and should be a superuser

@login_required(login_url="/accounts/login")
def products(request):
    context = {}
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        products = Product.objects.all().order_by('-created')
        if form.cleaned_data['name']:
            products = products.filter(
                name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['available']:
            products = products.filter(
                available=form.cleaned_data['available'])
        if form.cleaned_data['published']:
            products = products.filter(
                published=form.cleaned_data['published'])
        # there is one way, find out
        context['products'] = products
        context['form'] = form
    else:
        products = request.user.sellerprofile.stock.all().order_by('-created')
        context['products'] = products
        context['form'] = form
    return render(request, 'achironet_admin/products.html', context)

class ProductDetailView(DetailView, LoginRequiredMixin):

    template_name = 'achironet_admin/product/detail.html'
    model = Product
    context_object_name = 'product'
    login_url = "/accounts/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = self.object.images.all().order_by('uploaded_at')
        try:
            context['first'] = images[0]
            context['second'] = images[1]
            context['third'] = images[2]
            context['fourth'] = images[3]
            context['fifth'] = images[4]
        except Exception:
            pass
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this product
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            print(ex)
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)

@login_required(login_url="/accounts/login")
def upload_image(request):
    # check if this is a post request
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return JsonResponse({"image_id": image.pk, "url": image.file.url})
        else:
            return HttpResponseBadRequest()

# delete_images


def delete_images(request):
    # check if this is a post request
    if request.method == "POST":
        form = DeleteImagesForm(request.POST)
        if form.is_valid():
            # do the processing
            if form.cleaned_data['delete_image_1']:
                # delete the image one
                try:
                    ProductImage.objects.get(
                        pk=form.cleaned_data['delete_image_1']).delete()
                    print("Image gone")
                except Exception as ex:
                    print(ex)
            if form.cleaned_data['delete_image_2']:
                # delete the image 2
                try:
                    ProductImage.objects.get(
                        pk=form.cleaned_data['delete_image_2']).delete()
                except Exception as ex:
                    print(ex)
            if form.cleaned_data['delete_image_3']:
                try:
                    ProductImage.objects.get(
                        pk=form.cleaned_data['delete_image_3']).delete()
                except Exception as ex:
                    print(ex)
            if form.cleaned_data['delete_image_4']:
                try:
                    ProductImage.objects.get(
                        pk=form.cleaned_data['delete_image_4']).delete()
                except Exception as ex:
                    print(ex)
            if form.cleaned_data['delete_image_5']:
                try:
                    ProductImage.objects.get(
                        pk=form.cleaned_data['delete_image_5']).delete()
                except Exception as ex:
                    print(ex)
            return JsonResponse({"message": "Success", "success": True})
    return JsonResponse({"message": "Nothing to delete", "success": False})
# Add product images


@login_required(login_url="/accounts/login")
def add_product_images(request, pk):
    context = {
        'product_image_form': ProductImageForm(),
        'delete_images_form': DeleteImagesForm(),
        'form': AssignProductImagesForm(),
        'is_mobile': mobile(request)
    }
    try:
        product = Product.objects.get(pk=pk)
        context['product'] = product
        if request.method == "POST":
            form = AssignProductImagesForm(request.POST)
            # validate form
            if form.is_valid():
                image_ids = []
                image_ids.append(form.cleaned_data['image_1'])
                image_ids.append(form.cleaned_data['image_2'])
                image_ids.append(form.cleaned_data['image_3'])
                image_ids.append(form.cleaned_data['image_4'])
                image_ids.append(form.cleaned_data['image_5'])
                # process the list
                for image_id in image_ids:
                    try:
                        product_image = ProductImage.objects.get(pk=image_id)
                        product_image.product = product
                        product_image.save()
                    except Exception as ex:
                        messages.error(
                            request, "An error occured: Images could not be added.")
                        return redirect("achironet_admin:add_product_images", pk=product.pk)
                return redirect("achironet_admin:create_overview", pk=product.pk)

    except Product.DoesNotExist:
        messages.info(request, "Product doesn't exist")
        return redirect("achironet_admin:http-404-not-found")

    return render(request, "achironet_admin/product/upload_product_images.html", context)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "achironet_admin/product/update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this product
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("achironet_admin:product_view", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'name': self.object.name,
            'category': self.object.category.pk,
            'description': self.object.description,
            'available': self.object.available,
            'stock': self.object.stock,
            'search_keywords': self.object.search_keywords,
        }
        # calculate the initial price
        inital_price = Decimal(Decimal(
            self.object.price) / Decimal(1.3)).quantize(Decimal('0.01'), rounding=ROUND_UP)
        data['price'] = inital_price
        form = ProductForm(data)
        context["form"] = form
        return context

    def form_valid(self, form):
        # Create a slug field
        self.object.slug = slugify(form.cleaned_data['name'])
        self.object.published = False
        self.object.price += Decimal(self.object.price) * Decimal(0.3)
        # Now save the object
        self.object.save()
        return super().form_valid(form)


@login_required(login_url="/accounts/login")
def edit_product_images(request, pk):
    context = {
        'product_image_form': ProductImageForm(),
        'delete_images_form': DeleteImagesForm(),
        'form': AssignProductImagesForm(),
        'is_mobile': mobile(request)
    }
    try:
        product = Product.objects.get(pk=pk)
        # security check
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            print(ex)
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        # ok user can now do what they want cuase they own this stuff
        context['product'] = product
        if request.method == "POST":
            form = AssignProductImagesForm(request.POST)
            # validate form
            if form.is_valid():
                product.images.all().delete()
                image_ids = []
                image_ids.append(form.cleaned_data['image_1'])
                image_ids.append(form.cleaned_data['image_2'])
                image_ids.append(form.cleaned_data['image_3'])
                image_ids.append(form.cleaned_data['image_4'])
                image_ids.append(form.cleaned_data['image_5'])
                # process the list
                for image_id in image_ids:
                    try:
                        product_image = ProductImage.objects.get(pk=image_id)
                        product_image.product = product
                        product_image.save()
                    except Exception as ex:
                        messages.error(
                            request, "An error occured: Images could not be added.")
                        return redirect("achironet_admin:add_product_images", pk=product.pk)
                return redirect("achironet_admin:product_view", pk=product.pk)

    except Product.DoesNotExist:
        return redirect("achironet_admin:http-404-not-found")

    return render(request, "achironet_admin/product/upload_update_product_images.html", context)


class OverviewCreateView(CreateView, LoginRequiredMixin):
    model = OverView
    template_name = 'achironet_admin/product/create_overview.html'
    form_class = OverViewForm
    login_url = "/accounts/login"

    def form_valid(self, form):
        # Create a slug field
        self.object = form.save(commit=False)
        product_id = int(self.kwargs['pk'])
        # Get the product
        product = Product.objects.get(pk=product_id)
        self.object.product = product
        # Now save the object
        self.object.save()
        return redirect("achironet_admin:create_specification", pk=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(pk=self.kwargs['pk'])
        return context


    def get(self, request, *args, **kwargs):
        # check if the user owns this product
        try:
            # get the product
            product_id = int(self.kwargs['pk'])
            product = Product.objects.get(pk=product_id)
            try:
                if request.user.sellerprofile.pk != product.seller.pk:
                    messages.info(
                        request, "Sorry, you are not allowed todo so.")
                    return redirect("shop:product_list")
            except Exception as ex:
                print(ex)
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Product.DoesNotExist:
            messages.info(request, "Product doesn't exist")
            return redirect("achironet_admin:http-404-not-found")
        return super().get(request, *args, **kwargs)


class OverviewUpdateView(UpdateView, LoginRequiredMixin):
    model = OverView
    template_name = 'achironet_admin/product/update_overview.html'
    form_class = OverViewForm
    login_url = "/accounts/login"

    def get_success_url(self):
        return reverse("achironet_admin:product_view", kwargs={"pk": self.object.product.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this product
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)


@login_required(login_url="/accounts/login")
def create_specification(request, pk):
    form = SpecificationForm()
    context = {}
    # security check
    try:
        product = Product.objects.get(pk=pk)
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        context['product'] = product
    except Product.DoesNotExist:
        messages.info("Sorry, product not found.")
        return redirect("achironet_admin:http-404-not-found")

    if request.method == "POST":
        form = SpecificationForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # get the product first
            product_id = int(pk)
            try:
                product = Product.objects.get(pk=product_id)
                # create new specification
                specification = Specification.objects.create(
                    product=product
                )
                # specification object created now give attributes
                attributes = json.loads(form.cleaned_data['attributes'])
                for attribute in attributes:
                    Attribute.objects.create(
                        specification=specification,
                        key=attribute['key'],
                        value=attribute['value']
                    )
                # If successful redirect to the product view
                return redirect("achironet_admin:product_view", pk=product_id)
            except Product.DoesNotExist:
                messages.info(request, "Sorry, product not found.")
                return redirect("achironet_admin:http-404-not-found")

    context['form'] = form
    return render(request, 'achironet_admin/product/create_specification.html', context)

# Edit the specification


@login_required(login_url="/accounts/login")
def update_specification(request, pk):
    form = SpecificationForm()
    # get the specification
    specification_id = int(pk)
    specification = None
    try:
        specification = Specification.objects.get(pk=specification_id)
        try:
            if not request.user.is_superuser:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
    except Specification.DoesNotExist:
        messages.info(request, "Spefication doesn't exist")
        return redirect("achironet_admin:http-404-not-found")

    if request.method == "POST":
        form = SpecificationForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # delete the old attributes
            specification.attribute_set.all().delete()
            # now add newly created attributes
            attributes = json.loads(form.cleaned_data['attributes'])
            for attribute in attributes:
                Attribute.objects.create(
                    specification=specification,
                    key=attribute['key'],
                    value=attribute['value']
                )
            # If successful redirect to the product view
            return redirect("achironet_admin:product_view", pk=specification.product.pk)

    context = {'form': form, 'specification': specification}
    return render(request, 'achironet_admin/product/update_specification.html', context)


@login_required(login_url="/accounts/login")
def sellers(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    sellers = SellerProfile.objects.all().order_by('-created')
    form = SellerFilterForm(request.GET)
    if form.is_valid():
        # process the data
        if form.cleaned_data['firstname']:
            sellers = sellers.filter(
                firstname__contains=form.cleaned_data['firstname'])
        if form.cleaned_data['lastname']:
            sellers = sellers.filter(
                lastname__contains=form.cleaned_data['lastname'])
    context = {
        'sellers': sellers,
        'form': form
    }
    return render(request, "achironet_admin/sellers.html", context)


@login_required(login_url="/accounts/login")
def orders(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    # now make a queryset to get the orders
    orders = Order.objects.all().order_by('-created')
    form = OrderFilterForm(request.GET)
    if form.is_valid():
        # process data
        if form.cleaned_data['name']:
            # filter orders using name
            orders = orders.filter(name__contains=form.cleaned_data['name'])
        if form.cleaned_data['start_date'] and form.cleaned_data['end_date']:
            orders = orders.filter(
                created__gte=form.cleaned_data['start_date'],
                created__lte=form.cleaned_data['end_date']
            )
        if form.cleaned_data['paid']:
            orders = orders.filter(
                paid=form.cleaned_data['paid']
            )
    context = {
        'orders': orders,
        'form': form
    }
    return render(request, "achironet_admin/orders.html", context)


@login_required(login_url="/accounts/login")
def change_items(request):
    print("Request made here")
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    payload = {}
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body)
            # validate the form
            form = ChangeItemForm(data)
            if form.is_valid():
                # process data
                item_id = form.cleaned_data['item_id']
                # now get the item
                try:
                    item = OrderItem.objects.get(pk=item_id)
                    if item.received == False:
                        item.received = True
                        item.save()
                        payload['received'] = True
                    else:
                        item.received = False
                        item.save()
                        payload['received'] = False

                    payload['success'] = True
                    payload['item_id'] = item.pk
                    return JsonResponse(payload)
                except OrderItem.DoesNotExist:
                    return JsonResponse({"success": False})
        except json.JSONDecodeError:
            print("Error must be happening here")
            return JsonResponse({"success": False})

    return JsonResponse({"message": "Ooops nothing for you here"})


# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def buyers(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    customers = Profile.objects.all().order_by('pk')
    form = CustomerFilterForm(request.GET)
    if form.is_valid():
        # process the data
        if form.cleaned_data['firstname']:
            customers = customers.filter(
                firstname__contains=form.cleaned_data['firstname'])
        if form.cleaned_data['lastname']:
            customers = customers.filter(
                lastname__contains=form.cleaned_data['lastname'])
    context = {
        'customers': customers,
        'form': form
    }

    return render(request, "achironet_admin/buyers.html", context)

# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def email_newsletters(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    # get all the email newsletters order by the last sent
    newsletters = EmailNewsletter.objects.all().order_by('-updated')
    context = {'newsletters': newsletters}
    return render(request, "achironet_admin/email_newsletters.html", context)

# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def create_email_newsletter(request):
    # deny access to a user who is not a super user
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    form = EmailNewsletterForm()
    # now check if this is a post request
    if request.method == "POST":
        # now validate the data
        form = EmailNewsletterForm(request.POST)
        if form.is_valid():
            # now send the email to all the registered sellers
            sellers = SellerProfile.objects.all()
            recipient_list = []
            for seller in sellers:
                recipient_list.append(seller.email)
            if len(recipient_list) > 0:
                try:
                    send_mail(
                        subject="Achironet market place: " +
                        form.cleaned_data['subject'],
                        message='Achironet market place news',
                        from_email='admin@achironetmarketplace.com',
                        recipient_list=recipient_list,
                        fail_silently=False,
                        html_message=form.cleaned_data['message']
                    )
                    # now save the newsletter for later purpose, since it has been
                    # sent
                    form.save()
                    messages.success(
                        request, "Your emails have been sent successfully")
                    return redirect("achironet_admin:email_newsletters")
                except Exception as ex:
                    print("/////////////////////////////////////////////")
                    print(ex)
                    print("/////////////////////////////////////////////")
                    messages.error(request, "Error sending email")
    return render(request, "achironet_admin/create_newsletter.html", {'form': form})


class EditEmailnewsletter(LoginRequiredMixin, UpdateView):
    model = EmailNewsletter
    form_class = EmailNewsletterForm
    template_name = "achironet_admin/edit_email_newsletter.html"
    login_url = "/accounts/login"

    def get_success_url(self):
        return reverse("achironet_admin:email_newsletters")

    def form_valid(self, form):
        # check if the user is a superuser
        if not self.request.user.is_superuser:
            return redirect("achironet_admin:http_404_not_available")
        # get the list
        sellers = SellerProfile.objects.all()
        recipient_list = []
        for seller in sellers:
            recipient_list.append(seller.email)
        if len(recipient_list) > 0:
            # try to send email
            try:
                send_mail(
                    "Achironet market place: " + form.cleaned_data['subject'],
                    'Achironet market place news',
                    'admin@achironetmarketplace.com',
                    recipient_list,
                    fail_silently=False,
                    html_message=form.cleaned_data['message']
                )
                messages.success(
                    self.request, "Your emails have been sent successfully")
            except Exception as ex:
                print("/////////////////////////////////////////////")
                print(ex)
                print("/////////////////////////////////////////////")
                messages.error(self.request, "Could not send emails")
                return redirect("achironet_admin:email_newsletters")
        return super().form_valid(form)


def delete_newsletter(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    # now check if this is a post request
    if request.method == "POST":
        # make a run for it
        form = None
        if settings.TESTING:
            form = DeleteEmailNewsletterForm(request.POST)
        else:
            data = json.loads(request.body)
            form = DeleteEmailNewsletterForm(data)
        # validate the form
        if form.is_valid():
            # process the data
            email_newsletter_id = int(form.cleaned_data['email_newsletter_id'])
            # now try to get the instance of the object
            try:
                email_newsletter = EmailNewsletter.objects.get(
                    pk=email_newsletter_id)
                email_newsletter.delete()
                return JsonResponse({
                    "message": "Successfully deleted",
                    "success": True,
                    "newsletter_id": email_newsletter_id
                })
            except EmailNewsletter.DoesNotExist:
                return HttpResponseNotFound()
    return JsonResponse({"message": "Nothing done", "success": False})


@login_required(login_url="/accounts/login")
def request_testmonials(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    context = {}
    context['groups'] = RequestReviewGroup.objects.all()
    return render(request, "achironet_admin/request_testmonials.html", context)


@login_required(login_url="/accounts/login")
def seller_testmonials(request):
    # deny access to is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    testmonials = Testmonial.objects.filter(published=False)
    context = {}
    context['testmonials'] = Testmonial.objects.all().filter(published=False)
    return render(request, "achironet_admin/seller_testmonials.html", context)


def mail_sellers(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    # now do the mail sending to the user
    hostname = request.get_host()
    testmonials_url = reverse("shop:sell_online")
    testmonials_url += "#testimonials"
    create_testmonial_url = reverse("users:create_testmonial")
    subject = "Achironet market place is asking for your help?"
    message = "<div style='font-size:18px'>"
    message += "<p>We have a quick favor to ask.</p>"
    message += "<p>Could you write a brief testimonial that I can add to my list of satisfied</p>"
    message += "<p>clients?</p>"
    message += "<p>I’m not looking for a novel or anything. Just a few sentences describing</p>"
    message += "<p>your experience with me. Prospective clients don’t care so much about</p>"
    message += "<p>what I say about myself, but they do care what my clients have to say.</p>"
    message += "<p><br>For an idea of what other clients have written, please "
    message += "<a href='https://{0}/{1}'>click here</a>".format(
        hostname, testmonials_url)
    message += "<br></p>"
    message += "<p>All you have to do is simply  visit "
    message += "<a href='https://{0}/{1}'>here</a>. Also</p>".format(
        hostname, create_testmonial_url)
    message += "<p>if you are able to do this in the next day or two, that would be awesome.</p>"
    # now it's time to send an email
    if request.method == "POST":

        # now get the group id
        form = None
        if settings.TESTING:
            form = RequestReviewForm(request.POST)
        else:
            # deserialize the the json data
            data = json.loads(request.body)
            form = RequestReviewForm(data)
        # check if the form is valid
        if form.is_valid():
            # then process the data
            group_id = int(form.cleaned_data['group_id'])
            # now get the group
            try:
                group = RequestReviewGroup.objects.get(pk=group_id)
                # now make a run for it
                sellers = group.sellerprofile_set.all()
                recepient_list = []
                if sellers.count() > 0:
                    # send emails to these sellers based on the criteria
                    # that this seller has been on site for a month
                    # if not then skip this seller
                    for seller in sellers:
                        today = datetime.now()
                        if (today.month - seller.created.month) >= 1:
                            recepient_list.append(seller.email)
                            group.sellerprofile_set.remove(seller)

                # now check if the group no longer contains anyone and remove it
                deleted_group = False
                if group.sellerprofile_set.all().count() == 0:
                    group.delete()
                    deleted_group = True
                # now that the receipient list has been update let's send those emails
                print(len(recepient_list))
                if len(recepient_list) > 0:
                    # then send emails
                    try:
                        send_mail(
                            subject,
                            "Achironet market place is asking for your help",
                            'admin@achironetmarketplace.com',
                            recepient_list,
                            fail_silently=False,
                            html_message=message
                        )
                        return JsonResponse(
                            {
                                'message': 'Emails successfully sent',
                                'success': True,
                                'deleteGroup': deleted_group,
                                'group_id': group_id
                            })
                    except Exception as ex:
                        return HttpResponseServerError()

            except RequestReviewGroup.DoesNotExist:
                return HttpResponseNotFound()
    return JsonResponse({'message': 'All the users haven\'t used the system for more than a month', 'success': True})


def delete_testmonial(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    # else check if this is a post request
    if request.method == "POST":
        form = None
        if settings.TESTING:
            form = ModerateTestmonialForm(request.POST)
        else:
            data = json.loads(request.body)
            form = ModerateTestmonialForm(data)
            # validate form
            if form.is_valid():
                # process data
                testmonial_id = int(form.cleaned_data['testmonial_id'])
                # now try to get the testmonial
                try:
                    testimonial = Testmonial.objects.get(pk=testmonial_id)
                    testimonial.delete()
                    return JsonResponse({
                        "message": "Deleted successfully",
                        "success": True,
                        "testmonial_id": testmonial_id
                    }
                    )
                except Testmonial.DoesNotExist:
                    return HttpResponseNotFound()
    return JsonResponse({"message": "Nothing done"})


def approve_testmonial(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    # else check if this is a post request
    if request.method == "POST":
        form = None
        if settings.TESTING:
            form = ModerateTestmonialForm(request.POST)
        else:
            data = json.loads(request.body)
            form = ModerateTestmonialForm(data)
            # validate form
            if form.is_valid():
                # process data
                testmonial_id = int(form.cleaned_data['testmonial_id'])
                # now try to get the testmonial
                try:
                    testimonial = Testmonial.objects.get(pk=testmonial_id)
                    testimonial.published = True
                    testimonial.save()
                    return JsonResponse({
                        "message": "Approved successfully",
                        "success": True,
                        "testmonial_id": testmonial_id
                    })
                except Testmonial.DoesNotExist:
                    return HttpResponseNotFound()
    return JsonResponse({"message": "Nothing done"})

# page not found


def http_404_not_available(request):
    return render(request, "achironet_admin/404.html", {})

def seller_revenue_claims(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    # now make a queryset to get the orders
    claims = Revenue.objects.all().filter(claimed=True).order_by('created')
    form = RevenueFilterForm(request.GET)
    if form.is_valid():
        # process data
        if form.cleaned_data['month']:
            # filter orders using name
            claims = claims.filter(month__contains=form.cleaned_data['month'])
        if form.cleaned_data['start_date'] and form.cleaned_data['end_date']:
            claims = claims.filter(
                created__gte=form.cleaned_data['start_date'],
                created__lte=form.cleaned_data['end_date']
            )
        if form.cleaned_data['paid']:
            claims = claims.filter(
                paid=form.cleaned_data['paid']
            )
    context = {
        'claims': claims,
        'form': form
    }
    return render(request, "achironet_admin/seller_claims.html", context)

class ClaimPaidUpdateView(UpdateView):
    fields = [
        'paid'
    ]
    template_name = "achironet_admin/claim_paid_update.html"
    model = Revenue

    def get_success_url(self):
        return reverse("achironet_admin:claim_update", kwargs={"pk": self.kwargs["pk"]})
