from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import reverse, redirect
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import ProfileForm, SellerProfileForm
from .models import Profile, SellerProfile
from django.contrib.auth.decorators import login_required

# Create your views here.


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
        'form': form
    }
    return render(request, 'users/setup_profile.html', context)


# User profile view
class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.all()
        return context

 # Edit user profile


class UpdateProfileView(UpdateView):
    model = Profile
    fields = ['profile_picture']
    template_name = 'users/profile_update_form.html'

    def get_success_url(self):
        pk = self.request.user.profile.pk
        return reverse('users:profile', kwargs={'pk': pk})


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
            # Finally save to the database
            profile.save()
            # return a redirect to the seller profile page
            return redirect("sell:dashboard")
    context = {
        'form': form
    }
    return render(request, 'users/setup_seller_profile.html', context)


# User profile view
class SellerProfileView(DetailView):
    model = SellerProfile
    template_name = "users/seller_profile.html"
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.stock.all()
        print(context['products'])
        return context

 # Edit seller profile


class UpdateSellerProfileView(UpdateView):
    model = SellerProfile
    fields = [
        'tradename',
        'phone_number',
        'email',
        'city',
        'state',
        'address',
        'bank_account',
        'brand_logo'
    ]
    template_name = 'users/seller_profile_update_form.html'

    def get_success_url(self):
        pk = self.request.user.sellerprofile.pk
        return reverse('users:seller-profile', kwargs={'pk': pk})
