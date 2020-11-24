from django import forms
from .models import Profile, SellerProfile, Testmonial
from shop.models import Review


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'score',
            'your_message'
        ]
        widgets = {
            'score': forms.HiddenInput()
        }


class TestmonialForm(forms.ModelForm):
    class Meta:
        model = Testmonial
        fields = [
            'fullname',
            'your_say',
            'score'
        ]

        widgets = {
            'score': forms.HiddenInput(),

        }