from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from order.models import Order
from shop.models import Product
from users.models import SellerProfile
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.utils.text import slugify
# Create your views here.

# This view should be guarded by a decorator, so that only an authorized user can view
@login_required(login_url="/accounts/login")
def dashboard(request):
    context = {}
    orders = request.user.sellerprofile.customer_orders.all().order_by(
        '-created')[:5]
    context['orders'] = orders
    context['order_count'] = orders.count()
    print(orders)
    products = request.user.sellerprofile.stock.all().order_by('-created')[:5]
    context['products'] = products
    return render(request, "sell/dashboard.html", context)

# This view should be guarded by a decorator, so that only an authorized user can view
def products(request):
    context = {}
    products = request.user.sellerprofile.stock.all().order_by('-created')
    context['products'] = products
    return render(request,'sell/products.html', context)

# This view should be guarded by a decorator, so that only an authorized user can view
def orders(request):
    context = {}
    orders = request.user.sellerprofile.customer_orders.all().order_by('-created')
    context['orders'] = orders
    return render(request, 'sell/orders.html', context)

# This view should be guarded by a decorator, so that only an authorized user can view
def revenue(request):
    context = {}
    sales = request.user.sellerprofile.sales.all().order_by('-created')
    context['sales'] = sales
    return render(request, 'sell/revenue.html', context)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'sell/order_details.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all().filter(seller=self.request.user.sellerprofile)
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


class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        'name',
        'image',
        'description',
        'price',
        'stock'
    ]
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
