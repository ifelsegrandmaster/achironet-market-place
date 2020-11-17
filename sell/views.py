from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import Revenue
from order.models import Order
from shop.models import Product, OverView, Specification, Attribute
from users.models import SellerProfile
from shop.forms import OverViewForm, SpecificationForm, ProductForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.utils.text import slugify
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
import json
from .encoders import DecimalEncoder
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
    products = request.user.sellerprofile.stock.all().order_by('-created')
    context['products'] = products
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
        return redirect("sell:create_overview", pk=self.object.pk)


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
