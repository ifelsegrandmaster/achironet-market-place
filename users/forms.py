from PIL import Image
from django.core.files import File
from django import forms
from .models import Profile, SellerProfile, Testmonial, Photo
from shop.models import Review

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname',
            'lastname',
        ]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            "profile_picture": forms.HiddenInput()
        }

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


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )
        labels ={
            "file": "Upload profile picture"
        }

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((512, 512), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
