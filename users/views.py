import re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import (
    ProfileForm,
    SellerProfileForm,
    ReviewForm,
    TestmonialForm,
    PhotoForm,
    UpdateProfileForm,
    UpdateSellerProfileForm
)
from .models import Profile, SellerProfile, Testmonial, RequestReviewGroup
from shop.models import Review, Product
from agent.models import AgentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# check if device is mobile


def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

# Create your views here.


@login_required(login_url="/accounts/login")
def choose_path(request):
    context = {}
    if request.method == "GET":
        try:
            Profile.objects.get(user=request.user)
            return redirect("shop:product_list")
        except Profile.DoesNotExist:
            pass
        # Check if a user has already have a shop profile
        try:
            SellerProfile.objects.get(user=request.user)
            return redirect("shop:product_list")
        except SellerProfile.DoesNotExist:
            pass
        # Check if a user has already have a sellerprofile
        try:
            AgentProfile.objects.get(user=request.user)
            return redirect("shop:product_list")
        except AgentProfile.DoesNotExist:
            pass

    testmonials = Testmonial.objects.filter(
        published=True).order_by("-created")
    context['testmonials'] = testmonials
    return render(request, "users/choose_path.html", context)


@login_required(login_url="/accounts/login")
def create_user_profile(request):
    form = ProfileForm()

    if request.method == "GET":
        try:
            Profile.objects.get(user=request.user)
            return redirect("shop:product_list")
        except Profile.DoesNotExist:
            pass

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Just get the Profile instance do not make any commitment to database
            profile = form.save(commit=False)
            # Now update the user
            profile.user = request.user
            # Finally save to the database
            profile.save()
            # return a redirect to the profile page
            return redirect("users:profile", pk=profile.pk)

    context = {
        'form': form,
        'is_mobile': mobile(request),
        'photo_form': PhotoForm()
    }
    return render(request, 'users/setup_profile.html', context)

# upload photo function


def upload_photo(request):
    # check if this is a post request
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            return JsonResponse({"photo_id": photo.pk, "url": photo.file.url})
        else:
            return HttpResponseBadRequest()


# User profile view
class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.all()
        return context

 # Edit user profile


class UpdateProfileView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = UpdateProfileForm
    login_url = 'acccounts/login/'
    template_name = 'users/profile_update.html'

    def get_success_url(self):
        pk = self.request.user.profile.pk
        return reverse('users:profile', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this profile
        try:
            if request.user.profile.pk != self.object.pk:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # check if the user is correct one
        context["photo_form"] = PhotoForm()
        context['is_mobile'] = mobile(self.request)
        return context


# Create a seller profile
@login_required(login_url="/accounts/login")
def create_seller_profile(request):
    form = SellerProfileForm()
    if request.method == 'GET':
        try:
            SellerProfile.objects.get(user=request.user)
            return redirect("sell:dashboard")
        except SellerProfile.DoesNotExist:
            pass

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Just get the SellerProfile instance do not make any commitments to database
            profile = form.save(commit=False)
            # Now update the user
            profile.user = request.user
            # add the seller to the request review group
            try:
                group = RequestReviewGroup.objects.latest("created")
                if group.sellerprofile_set.all().count() < 50:
                    profile.review_group = group
                else:
                    # create a new group
                    goup = RequestReviewGroup.objects.create()
                    profile.review_group = group

            except RequestReviewGroup.DoesNotExist:
                group = RequestReviewGroup.objects.create()
                profile.review_group = group
            # Finally save to the database
            profile.save()
            # return a redirect to the seller profile page
            return redirect("users:upload_seller_profile_picture", pk=profile.pk)
    context = {
        'form': form,
        'is_mobile': mobile(request),
        'photo_form': PhotoForm()
    }
    return render(request, 'users/setup_seller_profile.html', context)

def upload_seller_profile_picture(request, pk):
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
                profile = SellerProfile.objects.get(pk=pk)
                profile.brand_logo = photo
                profile.save()
                return redirect("sell:dashboard")
            except SellerProfile.DoesNotExist:
                messages.error(request, "Error could not upload image for non-existent profile.")

    return render(request, "users/upload_profile.html", context)

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
                profile = Profile.objects.get(pk=pk)
                profile.profile_picture = photo
                profile.save()
                return redirect("users:profile", pk=profile.pk)
            except Profile.DoesNotExist:
                messages.error(request, "Error could not upload image for non-existent profile.")

    return render(request, "users/upload_profile.html", context)

@login_required(login_url="/accounts/login")
def product_review(request, pk):
    form = ReviewForm()
    # first get the product of the review
    product_id = int(pk)
    product = None
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return redirect("users:http_404_not_found")
    # now check if there is a review that exists
    review = None
    profile = request.user.profile
    data = {}
    try:
        review = profile.review_set.get(product=product)
        data['your_message'] = review.your_message
        data['score'] = review.score
        form = ReviewForm(data)
        # check if this is a POST request
        if request.method == "POST":
            # create a new review form bounded with post data
            form = ReviewForm(request.POST)
            # check if the form is valid
            if form.is_valid():
                # do the processing
                score = int(form.cleaned_data['score'])
                your_message = form.cleaned_data['your_message']
                # now update the review data
                review.your_message = your_message
                review.score = score
                review.save()
                return redirect(product)

    except Review.DoesNotExist:
        # If a review does not exist then create a new one
        # check if this is a post request
        if request.method == "POST":
            form = ReviewForm(request.POST)
            # check if the form is valid
            if form.is_valid():
                # do the processing
                score = int(form.cleaned_data['score'])
                your_message = form.cleaned_data['your_message']
                Review.objects.create(
                    product=product,
                    user_profile=profile,
                    score=score,
                    your_message=your_message
                )
                return redirect(product)
    context = {'form': form, 'review': review}
    return render(request, "users/create_or_edit_review.html", context)


# User profile view
@login_required(login_url="/accounts/login")
def create_testmonial(request):
    context = {}
    # get the form
    form = TestmonialForm()
    # check if this is a post method
    if request.method == "POST":
        form = TestmonialForm(request.POST, request.FILES)
        if form.is_valid():
            # process data
            testimonial = form.save(commit=False)
            try:
                testimonial.seller = request.user.sellerprofile
                testimonial.save()
                messages.info(request, "Thank you for your testimony")
                return redirect("shop:product_list")
            except Exception as ie:
                messages.info(
                    request, "Could not testify, you need to be a seller todo that")
                return redirect("shop:product_list")
    context['form'] = form
    return render(request, "users/create_testmonial.html", context)


class SellerProfileView(DetailView):
    model = SellerProfile
    template_name = "users/seller_profile.html"
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.stock.all()
        try:
            if self.request.user.sellerprofile == self.object:
                context['can_edit'] = True
        except Exception:
            pass
        return context

 # Edit seller profile


class UpdateSellerProfileView(UpdateView, LoginRequiredMixin):
    model = SellerProfile
    form_class = UpdateSellerProfileForm
    login_url = "accounts/login/"
    template_name = 'users/seller_profile_update_form.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # check if the user owns this profile
        try:
            if request.user.sellerprofile.pk != self.object.pk:
                messages.info(request, "Sorry, you are not allowed todo so.")
                return redirect("shop:product_list")
        except Exception:
            messages.info(request, "Sorry, you are not allowed todo so.")
            return redirect("shop:product_list")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.request.user.sellerprofile.pk
        return reverse('users:seller-profile', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo_form"] = PhotoForm()
        context["is_mobile"] = mobile(self.request)
        return context


# A 404 not found page
def http_404_not_found(request):
    response = render(request, 'sell/404.html', {})
    response.status_code = 404
    return response
