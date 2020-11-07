from django import forms
from .models import Profile, SellerProfile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname',
            'lastname',
            'profile_picture',
        ]

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            'tradename',
            'firstname',
            'lastname',
            'phone_number',
            'email',
            'city',
            'state',
            'address',
            'bank_account',
            'brand_logo'
        ]