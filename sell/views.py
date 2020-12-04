from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import Revenue
from order.models import Order
from shop.models import Product, OverView, Specification, Attribute, ProductImage
from users.models import SellerProfile
from shop.forms import (OverViewForm, SpecificationForm,
                        ProductForm, ProductImageForm, AssignProductImagesForm, DeleteImagesForm)
from .forms import ProductFilterForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.text import slugify
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
import json
import re
from .encoders import DecimalEncoder
from django.http import HttpResponseBadRequest
# Create your views here.

# This view should be guarded by a decorator, so that only an authorized user can view
MONTHS = dict([
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
])

# check if device is mobile


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
    context = {}
    orders = request.user.sellerprofile.customer_orders.all().order_by(
        '-created')[:5]
    context['orders'] = orders
    context['order_count'] = request.user.sellerprofile.customer_orders.all().count()
    products = request.user.sellerprofile.stock.all().order_by('-created')[:5]
    context['products'] = products

    # Get the latest revenue object
    latest = None
    try:
        latest = request.user.sellerprofile.sales.latest('created')
    except Revenue.DoesNotExist:
        # Create a new one since the customer is a new one
        today = datetime.now()
        latest = Revenue.objects.create(
            month=MONTHS[today.month],
            products_sold=0,
            sales=0,
            seller=request.user.sellerprofile,
            year=str(today.year)
        )

    context['latest'] = latest
    return render(request, "sell/dashboard.html", context)

# This view should be guarded by a decorator, so that only an authorized user can view


def products(request):
    context = {}
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        products = request.user.sellerprofile.stock.all().order_by('-created')
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
    return render(request, 'sell/products.html', context)

# This view should be guarded by a decorator, so that only an authorized user can view


def orders(request):
    context = {}
    orders = request.user.sellerprofile.customer_orders.all().order_by('-created')
    context['orders'] = orders
    return render(request, 'sell/orders.html', context)

# This view should be guarded by a decorator, so that only an authorized user can view


def revenue(request):
    # just always get the last object as the recent
    # the object created recently is the one which is
    # the recent most
    context = {}
    sales = request.user.sellerprofile.sales.all().order_by('-created')
    latest = None
    try:
        latest = request.user.sellerprofile.sales.latest('created')
    except Revenue.DoesNotExist:
       # Create a new one since the customer is a new one
        today = datetime.now()
        latest = Revenue.objects.create(
            month=MONTHS[today.month],
            products_sold=0,
            sales=0,
            seller=request.user.sellerprofile,
            year=str(today.year)
        )
    latest_revenue_creation_date = latest.created
    today = datetime.now()
    # Now compare the two dates
    if today.month > latest_revenue_creation_date.month:
        if today.day > latest_revenue_creation_date.day:
            # Then now create a new revenue data object
            latest = Revenue.objects.create(
                month=MONTHS[today.month],
                products_sold=0,
                sales=0,
                seller=request.user.sellerprofile,
                year=str(today.year)
            )

    context['sales'] = sales
    context['latest'] = latest
    return render(request, 'sell/revenue.html', context)

# View extra details of revenue for a certain month


class RevenueDetailView(DetailView):
    model = Revenue
    template_name = 'sell/revenue_details.html'
    context_object_name = 'revenue'

# This view should be protected by a decorator, so  that only an authorized user can view


def get_revenue_data(request):
    context = {}
    sales = (request.user.sellerprofile.sales.all().order_by('created')
             .values('month', 'products_sold', 'sales'))
    sales_list = [revenue for revenue in sales]
    # Now serialize into json
    data = json.dumps(list(sales_list), cls=DecimalEncoder)
    context['data'] = data
    return JsonResponse(context)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'sell/order_details.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all().filter(
            seller=self.request.user.sellerprofile)
        return context


# A 404 not found page
def http_404_not_found(request):
    response = render(request, 'sell/404.html', {})
    response.status_code = 404
    return response


class ProductDetailView(DetailView):

    template_name = 'sell/product/detail.html'
    model = Product
    context_object_name = 'product'

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



class ProductCreateView(CreateView):
    model = Product
    template_name = 'sell/product/create.html'
    form_class = ProductForm

    def get_success_url(self):
        return reverse("sell:products")

    def form_valid(self, form):
        # Create a slug field
        self.object = form.save(commit=False)
        self.object.slug = slugify(form.cleaned_data['name'])
        self.object.published = False
        self.object.seller = self.request.user.sellerprofile
        # Now save the object
        self.object.save()
        return redirect("sell:add_product_images", pk=self.object.pk)

# upload photo function


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
                        return redirect("sell:add_product_images", pk=product.pk)
                return redirect("sell:create_overview", pk=product.pk)

    except Product.DoesNotExist:
        return redirect("sell:http-404-not-found")

    return render(request, "sell/product/upload_product_images.html", context)


class OverviewCreateView(CreateView):
    model = OverView
    template_name = 'sell/product/create_overview.html'
    form_class = OverViewForm

    def form_valid(self, form):
        # Create a slug field
        self.object = form.save(commit=False)
        product_id = int(self.kwargs['pk'])
        # Get the product
        product = Product.objects.get(pk=product_id)
        self.object.product = product
        # Now save the object
        self.object.save()
        return redirect("sell:create_specification", pk=product_id)


class OverviewUpdateView(UpdateView):
    model = OverView
    template_name = 'sell/product/update_overview.html'
    form_class = OverViewForm

    def get_success_url(self):
        return reverse("sell:product_view", kwargs={"pk": self.object.product.pk})


def create_specification(request, pk):
    form = SpecificationForm()

    if request.method == "POST":
        form = SpecificationForm(request.POST)
        # check if form is valid
        if form.is_valid():
            # get the product first
            product_id = int(pk)
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
            return redirect("sell:product_view", pk=product_id)

    context = {'form': form}
    return render(request, 'sell/product/create_specification.html', context)

# Edit the specification


def update_specification(request, pk):
    form = SpecificationForm()
    # get the specification
    specification_id = int(pk)
    specification = None
    try:
        specification = Specification.objects.get(pk=specification_id)
    except Specification.DoesNotExist:
        return redirect("sell:http-404-not-found")

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
            return redirect("sell:product_view", pk=specification.product.pk)

    context = {'form': form, 'specification': specification}
    return render(request, 'sell/product/update_specification.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "sell/product/update.html"

    def get_success_url(self):
        return reverse("sell:product_view", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # Create a slug field
        self.object.slug = slugify(form.cleaned_data['name'])
        self.object.published = False
        # Now save the object
        self.object.save()
        return super().form_valid(form)
