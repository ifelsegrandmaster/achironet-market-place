from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import Revenue, BankDetails
from order.models import Order
from shop.models import Product, OverView, Specification, Attribute, ProductImage
from users.models import SellerProfile, Profile
from shop.forms import (OverViewForm, SpecificationForm,
                        ProductForm, ProductImageForm, AssignProductImagesForm, DeleteImagesForm)
from .forms import ProductFilterForm, ClaimMoneyForm, OrderFilterForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.text import slugify
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
import json
import re
from decimal import Decimal, ROUND_UP
from .encoders import DecimalEncoder
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
    # security check
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


@login_required(login_url="/accounts/login")
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


@login_required(login_url="/accounts/login")
def orders(request):
    context = {}
    orders = request.user.sellerprofile.customer_orders.filter(paid=True).order_by('created')
    form = OrderFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['name']:
            orders = orders.filter(name__contains=form.cleaned_data['name'])
        if form.cleaned_data['start_date'] and form.cleaned_data['end_date']:
            orders = orders.filter(
                Q(created__gte=form.cleaned_data['start_date']),
                Q(created__lte=form.cleaned_data['end_date'])
            )


    context['orders'] = orders
    context['form'] = form
    return render(request, 'sell/orders.html', context)

# This view should be guarded by a decorator, so that only an authorized user can view


@login_required(login_url="/accounts/login")
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


@login_required(login_url="/accounts/login")
def claim_money(request, pk):
    context = {}
    form = ClaimMoneyForm()
    context['form'] = form
    # check if this is a post request
    if request.method == "POST":
        form = ClaimMoneyForm(request.POST)
        if form.is_valid():
            # process the request
            try:
                revenue = request.user.sellerprofile.sales.get(pk=pk)
                # if found then process the transaction
                if revenue.claimed:
                    messages.info(
                        request, "Claim has already been made for {0}.".format(revenue.month))
                    return redirect("sell:revenue_view", pk=pk)
                if not revenue.is_claimable:
                    messages.info(
                        request, "Sorry you cannot claim money for  {0}.".format(revenue.month))
                    return redirect("sell:revenue_view", pk=pk)
                # create the bank details
                bank_details = BankDetails()
                bank_details.bank_name = form.cleaned_data['bank_name']
                bank_details.bank_account = form.cleaned_data['account_number']
                bank_details.save()
                revenue.bank_details = bank_details
                revenue.claimed = True
                revenue.save()
                messages.success(
                    request, "Claim has been made, money will be deposited into your bank account within 24 hours.")
                return redirect("sell:revenue_view", pk=pk)
            except Revenue.DoesNotExist:
                messages.error(
                    request, "Sorry could not find sales for that month.")
                return redirect("sell:http-404-not-found")
            except Exception as ex:
                print(ex)
                messages.error(request,
                               "An error occured while processing your request. Contact us if the problem persists.")
                return redirect("sell:claim_money", pk=pk)

    return render(request, "sell/claim_money.html", context)

# This view should be protected by a decorator, so  that only an authorized user can view


@login_required(login_url="/accounts/login")
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


class ProductDetailView(DetailView, LoginRequiredMixin):

    template_name = 'sell/product/detail.html'
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
            if (request.user.sellerprofile.pk != self.object.seller.pk) and ( not request.user.is_superuser):
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            print(ex)
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    template_name = 'sell/product/create.html'
    form_class = ProductForm
    login_url = "/accounts/login"

    def get_success_url(self):
        return reverse("sell:products")

    def form_valid(self, form):
        # Create a slug field
        self.object = form.save(commit=False)
        self.object.slug = slugify(form.cleaned_data['name'])
        self.object.published = False
        self.object.price += Decimal(self.object.price) * Decimal(0.3)
        self.object.seller = self.request.user.sellerprofile
        # Now save the object
        self.object.save()
        return redirect("sell:add_product_images", pk=self.object.pk)

# upload photo function


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
                        return redirect("sell:add_product_images", pk=product.pk)
                return redirect("sell:create_overview", pk=product.pk)

    except Product.DoesNotExist:
        messages.info(request, "Product doesn't exist")
        return redirect("sell:http-404-not-found")

    return render(request, "sell/product/upload_product_images.html", context)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "sell/product/update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this product
        try:
            if (request.user.sellerprofile.pk != self.object.seller.pk) and (not request.user.is_superuser):
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("sell:product_view", kwargs={"pk": self.object.pk})

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
            if (request.user.sellerprofile.pk != product.seller.pk) and (not request.user.is_superuser):
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
                        return redirect("sell:add_product_images", pk=product.pk)
                return redirect("sell:product_view", pk=product.pk)

    except Product.DoesNotExist:
        return redirect("sell:http-404-not-found")

    return render(request, "sell/product/upload_update_product_images.html", context)


class OverviewCreateView(CreateView, LoginRequiredMixin):
    model = OverView
    template_name = 'sell/product/create_overview.html'
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
        return redirect("sell:create_specification", pk=product_id)

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
                if (request.user.sellerprofile.pk != product.seller.pk) and ( not request.user.is_superuser):
                    messages.info(
                        request, "Sorry, you are not allowed todo so.")
                    return redirect("shop:product_list")
            except Exception as ex:
                print(ex)
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Product.DoesNotExist:
            messages.info(request, "Product doesn't exist")
            return redirect("sell:http-404-not-found")
        return super().get(request, *args, **kwargs)


class OverviewUpdateView(UpdateView, LoginRequiredMixin):
    model = OverView
    template_name = 'sell/product/update_overview.html'
    form_class = OverViewForm
    login_url = "/accounts/login"

    def get_success_url(self):
        return reverse("sell:product_view", kwargs={"pk": self.object.product.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this product
        try:
            if (request.user.sellerprofile.pk != self.object.product.seller.pk) and ( not request.user.is_superuser):
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
            if (request.user.sellerprofile.pk != product.seller.pk) and ( not request.user.is_superuser):
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        context['product'] = product
    except Product.DoesNotExist:
        messages.info("Sorry, product not found.")
        return redirect("sell:http-404-not-found")

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
                return redirect("sell:product_view", pk=product_id)
            except Product.DoesNotExist:
                messages.info(request, "Sorry, product not found.")
                return redirect("sell:http-404-not-found")

    context['form'] = form
    return render(request, 'sell/product/create_specification.html', context)

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
            if (request.user.sellerprofile.pk != specification.product.seller.pk) and ( not request.user.is_superuser):
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception as ex:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
    except Specification.DoesNotExist:
        messages.info(request, "Spefication doesn't exist")
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
