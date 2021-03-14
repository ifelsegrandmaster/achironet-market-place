from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import *
from sell.models import BankDetails
from .forms import CreateAgentForm
from .encoders import DecimalEncoder
from users.forms import PhotoForm
import re
import json
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


class AgentCreate(CreateView):
    model = AgentProfile
    form_class = CreateAgentForm
    template_name = "agent/create.html"

    def form_valid(self, form):
        # Create a slug field
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        # Now save the object
        self.object.save()
        return redirect("agent:upload_profile_picture", pk=self.object.pk)


def upload_profile_picture(request, pk):
    form = PhotoForm()
    context = {
        'form': form,
        'is_mobile': mobile(request)
    }
    if request.method == "POST":
        # validation
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            try:
                profile = AgentProfile.objects.get(pk=pk)
                profile.profile_picture = photo
                profile.save()
                return redirect("agent:profile", pk=profile.pk)
            except AgentProfile.DoesNotExist:
                messages.error(
                    request, "Error could not upload image for non-existent profile.")

    return render(request, "agent/upload_profile.html", context)

# User profile view


class ProfileView(DetailView):
    model = AgentProfile
    template_name = "agent/profile.html"


class ProfileUpdate(UpdateView):
    model = AgentProfile
    form_class = CreateAgentForm
    template_name = "agent/update.html"

    def get_success_url(self):
        return reverse("agent:profile", kwargs={"pk": self.object.pk})


@login_required(login_url="/accounts/login")
def dashboard(request):
    context = {}
    try:
        commission = request.user.agentprofile.commissions.latest('created')
        # now get the latest day
        try:
            day = commission.days.latest('date')
            context['earnings'] = day.earnings.all()
        except Day.DoesNotExist:
            pass
    except Commission.DoesNotExist:
        pass
    except AgentProfile.DoesNotExist:
        return redirect("agent:create-profile")
    return render(request, "agent/dashboard.html", context)


@login_required(login_url="/accounts/login")
def get_commission_data(request):
    context = {}
    try:
        commission = request.user.agentprofile.commissions.latest('created')
        # get graph data
        context['weekly_data'] = json.dumps(
            commission.get_weekly_data(), cls=DecimalEncoder)
        context['monthly_data'] = json.dumps(
            commission.get_monthly_data(), cls=DecimalEncoder)
        return JsonResponse(context)
    except Commission.DoesNotExist:
        return JsonResponse({
            'empty': True
        })
    except AgentProfile.DoesNotExist:
        return HttpResponseNotFound()


@login_required(login_url="/accounts/login")
def monthly_data(request):
    context = {}
    try:
        months = request.user.agentprofile.commissions.all().order_by('-created')
        context['months'] = months
    except AgentProfile.DoesNotExist:
        return redirect("agent:create-profile")
    return render(request, "agent/monthly_data.html", context)


@login_required(login_url="/accounts/login")
def get_yearly_graph_data(request):
    context = {}
    try:
        agent = request.user.agentprofile
        context['yearly_data'] = json.dumps(
            get_yearly_data(agent), cls=DecimalEncoder)
        return JsonResponse(context)
    except AgentProfile.DoesNotExist:
        return HttpResponseNotFound()

class MonthView(DetailView):
    model = Commission
    template_name = "agent/month_view.html"

class DayView(DetailView):
    model = Day
    template_name = "agent/day_view.html"


class BankDetailsCreate(CreateView):
    model = BankDetails
    template_name = "agent/create_bank_details.html"
    fields = [
        'bank_name',
        'bank_account'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['month'] = Commission.objects.get(pk=self.kwargs['pk'])
        except Exception:
            messages.error(self.request, "An error occured while retrieving the month data")
        return context

    def form_valid(self, form):
        month = Commission.objects.get(pk=self.kwargs['pk'])
        # if month has already been claimed then just redirect
        if month.claimed:
            messages.error(self.request, "Already claimed for this month.")
            return redirect("agent:view_month", pk=month.pk)
        # otherwise save the new data
        self.object = form.save()
        month.bank_details = self.object
        month.claimed = True
        month.save()
        return redirect("agent:view_month", pk=month.pk)