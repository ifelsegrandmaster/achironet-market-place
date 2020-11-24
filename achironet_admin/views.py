from django.shortcuts import render, redirect, reverse
from users.models import RequestReviewGroup
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import (
    HttpResponseForbidden,
    HttpResponseServerError,
    HttpResponseNotFound,
    JsonResponse
)
from .forms import RequestReviewForm
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
    context = {}
    return render(request, "achironet_admin/dashboard.html", context)

# List all the sellers who have registered
# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def sellers(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    context = {}
    return render(request, "achironet_admin/sellers.html", context)

# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def buyers(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    context = {}
    return render(request, "achironet_admin/buyers.html", context)

# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def email_newsletters(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    context = {}
    return render(request, "achironet_admin/email_newsletters.html", context)

# person should be logged in and should be a superuser


@login_required(login_url="/accounts/login")
def request_testmonials(request):
    # deny access to a user who is not a superuser
    if not request.user.is_superuser:
        return redirect("achironet_admin:http_404_not_available")
    context = {}
    context['groups'] = RequestReviewGroup.objects.all()
    return render(request, "achironet_admin/request_testmonials.html", context)


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
                            fail_silently=False
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

# page not found


def http_404_not_available(request):
    return render(request, "achironet_admin/404.html", {})
