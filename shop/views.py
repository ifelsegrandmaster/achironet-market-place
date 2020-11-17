from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product
from allauth.account.views import *

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]


class CustomAccountInactiveView(AccountInactiveView):
    template_name = 'allauth/account/account_inactive.html'


class CustomEmailConfirmView(ConfirmEmailView):
    template_name = 'allauth/account/email_confirm.html'


class CustomEmailView(EmailView):
    template_name = 'allauth/account/email.html'


class CustomLoginView(LoginView):
    template_name = 'allauth/account/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'allauth/account/logout.html'


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'allauth/account/password_change.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'allauth/account/password_reset_done.html'


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'allauth/account/password_reset_from_key_done.html'


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "allauth/account/password_reset_from_key.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "allauth/account/password_reset.html"


class CustomPasswordSetView(PasswordSetView):
    template_name = "allauth/account/password_set.html"


class CustomSignupView(SignupView):
    template_name = 'allauth/account/signup.html'


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category,
               'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)


def about(request):
    context = {'title': 'About'}
    return render(request, 'shop/about.html', context)


def contact(request):
    context = {'title': 'Contact us'}
    return render(request, 'shop/contact.html', context)


def sell_online(request):
    context = {'title': 'Sell online'}
    return render(request, 'shop/sell_online.html', context)

# class ProductListView(generic.ListView):
#     template_name = 'shop/product/list.html'

#     def get_queryset(self):
#         return Product.objects.filter(available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = None
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
#         context['categories'] = Category.objects.all()


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)


# class ProductDetialView(generic.DetailView):

#     template_name = 'shop/product/detail.html'
#     model = Product
#     form_class = CartAddProductForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = get_object_or_404(Product,
#         id=id, slug=slug, available=True)
#         return context
