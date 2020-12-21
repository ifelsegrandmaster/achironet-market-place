from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from .models import Category, Product, Review, SiteInformation
from users.models import Testmonial, Profile
from .forms import ContactForm, ApprovalForm, SearchForm
from order.models import Order, OrderItem
from allauth.account.views import *
from django.views.decorators.cache import never_cache
import json
import re

def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]
# check if device is mobile


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


def publish_product(request):
    payload = {'message': 'Oops nothing here'}
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        form = ApprovalForm(data)
        if form.is_valid():
            product_id = int(form.cleaned_data['product_id'])
            message_text = form.cleaned_data['message_text']
            # now get the product
            success = False
            message = ""
            hostname = request.get_host()
            try:
                product = Product.objects.get(pk=product_id)
                if product.published:
                    message += "<div style='font-size:18px'>"
                    message += "<p>Dear {0} ".format(
                        product.seller.firstname)
                    message += "your product "
                    message += "<a href='https://{0}/sell/view/product/{1}'><b>{2}</b></a>".format(
                        hostname, product.id, product.name)
                    message += "has been disapproved.</p>"
                    message += " <p><b>Reason: </b> {0}</p>".format(
                        message_text)
                    message += "<p>You can contact us on info@achironetmarketplace.com</p>"
                    message += "</div>"
                    # send email to the seller that a product has been disapproved
                    # send the email
                    try:
                        send_mail(
                            "Product disapproval on achironet market place.",
                            "Your product has been disapproved",
                            'admin@achironet.com',
                            [product.seller.email],
                            fail_silently=False,
                            html_message=message
                        )
                    except Exception as ex:
                        pass
                    product.published = False
                    payload['published'] = False
                    payload['message'] = "Product disapproved"
                else:
                    message = "<div style='font-size:18px'>"
                    message += "<p>Dear {0} ".format(
                        product.seller.firstname)
                    message += "your product "
                    message += "<a href='https://{0}/{1}/{2}'><b>{3}</b></a>".format(
                        hostname, product.id, product.slug, product.name)
                    message += " has been approved.</p>"
                    message += "<p>For more information email us on info@achironetmarketplace.com</p>"
                    message += "</div>"
                    # send email to the seller that a product has been disapproved
                    # send the email
                    try:
                        send_mail(
                            "Product approval on achironet market place.",
                            "Your product has been approved",
                            'admin@achironet.com',
                            [product.seller.email],
                            fail_silently=False,
                            html_message=message
                        )
                    except Exception as ex:
                        pass
                    product.published = True
                    payload['published'] = True
                    payload['message'] = 'Product approved'

                # Save the product
                product.save()
                success = True
                payload['success'] = success
                payload['product_id'] = product_id

            except Product.DoesNotExist:
                success = False
                message = "Product could not be found"
                payload['message'] = 'Product could not be found'
            except Exception:
                success = False
                # send email to the admin
                message = "An error has occured, we have been notified. Also contact the admin to remind them"
                payload['message'] = 'An error occured'
    return JsonResponse(payload)

@never_cache
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = None
    if request.user.is_staff:
        products = Product.objects.filter(available=True).order_by('-created')
    else:
        products = Product.objects.filter(
            available=True, published=True).order_by('-created')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # paginate the objects of 12 items each
    paginator = Paginator(products, 12)
    # now check if request.GET has pages
    current_page = 1
    if request.GET.get('page', None):
        # now get the page number
        page_number = int(request.GET.get('page'))
        products = paginator.page(page_number)
        current_page = page_number
    else:
        products = paginator.page(1)

    pages = [1]
    if paginator.num_pages > 1:
        pages = list(range(1, paginator.num_pages+1))
        print(paginator.num_pages)
        print(pages)
    context = {'category': category,
               'categories': categories,
               'products': products,
               'pages': pages,
               'current_page': current_page,
               'is_mobile': mobile(request)
               }
    # add extra values
    if products.has_previous():
        context['previous'] = products.previous_page_number()
    # next page
    if products.has_next():
        context['next'] = products.next_page_number()
    return render(request, 'shop/product/list.html', context)

# search products


def search_products(request):
    products = None
    if request.user.is_staff:
        products = Product.objects.filter(available=True)
    else:
        products = Product.objects.filter(available=True, published=True)
    # now filter the products based on search queryset
    form = SearchForm(request.GET)
    query_string = ""
    if form.is_valid():
        # now search the products
        products = products.search(**form.cleaned_data)
        query_string = form.cleaned_data['q']

    # create categories
    categories = []
    for product in products:
        categories.append(product.category)
    categories = set(categories)
    # paginate the objects of 12 items each
    paginator = Paginator(products, 12)
    # now check if request.GET has pages
    current_page = 1
    # check if page number was provided
    if request.GET.get('page', None):
        # now get the page number
        page_number = int(request.GET.get('page'))
        products = paginator.page(page_number)
        current_page = page_number
    else:
        products = paginator.page(1)

    pages = [1]
    if paginator.num_pages > 1:
        pages = list(range(1, paginator.num_pages+1))
        print(paginator.num_pages)
        print(pages)
    context = {
        'categories': categories,
        'products': products,
        'pages': pages,
        'current_page': current_page,
        'form': form,
        'query_string': query_string
    }
    # add extra values
    if products.has_previous():
        context['previous'] = products.previous_page_number()
    # next page
    if products.has_next():
        context['next'] = products.next_page_number()

    categories = set(categories)
    return render(request,
                  "shop/product/search.html",
                  context)


def contact(request):
    context = {'title': 'Contact us'}

    form = ContactForm()
    # check if this is a post request
    if request.method == "POST":
        form = ContactForm(request.POST)
        # validate
        if form.is_valid():
            # process
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']
            message = "Name: " + name + " \nPhone number: " + phone_number + " \n"
            message += body
            print("This happened")
            # send the email
            send_mail(
                subject,
                message,
                'admin@achironet.com',
                ['info@achironet.com'],
                fail_silently=False,
            )

            return redirect("shop:thanks")

    context['form'] = form
    try:
        siteinfo = SiteInformation.objects.latest('created')
        context['siteinfo'] = siteinfo
    except SiteInformation.DoesNotExist:
        pass

    return render(request, 'shop/contact.html', context)


def thanks(request):
    context = {
        'title': 'Thank you'
    }
    return render(request, "shop/thanks.html", context)


def sell_online(request):
    context = {'title': 'Sell online'}
    testmonials = Testmonial.objects.filter(
        published=True).order_by("-created")
    context['testmonials'] = testmonials
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
    user_can_review_product = False
    if request.user.is_authenticated:
        try:
            # check if the user has reviewed the product
            if request.user.profile:
                # first check if a person has purchased this item before
                orders = request.user.profile.orders.all()
                # now search for that product
                for order in orders:
                    # make a search in the order items
                    try:
                        orderitem = order.items.get(product=product)
                        user_can_review_product = True
                    except OrderItem.DoesNotExist:
                        pass
        except Profile.DoesNotExist:
            pass

    cart_product_form = CartAddProductForm()
    # get the related products
    seller = product.seller
    related_products = seller.stock.filter(
        published=True, available=True).order_by('?')[:10]
    context = {'product': product,
               'cart_product_form': cart_product_form,
               'user_can_review': user_can_review_product,
               'related_products': related_products,
               'is_mobile': mobile(request)
               }
    # get product images
    images = product.images.all().order_by('uploaded_at')
    try:
        context['first'] = images[0]
        context['second'] = images[1]
        context['third'] = images[2]
        context['fourth'] = images[3]
        context['fifth'] = images[4]
    except Exception:
        pass
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
