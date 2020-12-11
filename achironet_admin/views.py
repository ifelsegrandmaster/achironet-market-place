from django.shortcuts import render, redirect, reverse
from users.models import RequestReviewGroup, Testmonial, SellerProfile, Profile
from order.models import Order, OrderItem
from .models import EmailNewsletter
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    ChangeItemForm
)
from datetime import datetime
import json
from django.core.mail import send_mail
# Create your views here.

# the home dashboard, person should be logged in to view this
# a person should be a super_user to view this


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

# List all the sellers who have registered
# person should be logged in and should be a superuser


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

    return JsonResponse({"success": False})


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
