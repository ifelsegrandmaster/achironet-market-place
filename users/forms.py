from PIL import Image
from django.core.files import File
from django import forms
from .models import Profile, SellerProfile, Testmonial, Photo
from shop.models import Review
from django.core.validators import ValidationError

STATE_CHOICES = (
    ("Midlands", "Midlands"),
    ("Harare", "Harare"),
    ("Bulawayo", "Bulawayo"),
    ("Matebeleland South", "Matebeleland South"),
    ("Matebeland North", "Matebeleland North"),
    ("Masvingo", "Masvingo"),
    ("Manicaland", "Manicaland"),
    ("Mashonaland West", "Mashonaland West"),
    ("Mashonaland East", "Mashonaland East"),
    ("Mashonaland Central", "Mashonaland Central")
)


class AccountNumberField(forms.CharField):
    def validate(self, value):
        # check if this value is a valid zimbabwean bank account number
        super().validate(value)
        # now check if this is a valid numeric number
        try:
            account_number = int(value)
        except ValueError:
            raise ValidationError(
                ('Invalid value: %(value)s'),
                code='invalid',
                params={'value': value},
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname',
            'lastname',
            'profile_picture',
        ]
        widgets ={
            'profile_picture': forms.HiddenInput(),
            'firstname': forms.TextInput(attrs={'placeholder': 'Firstname'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Lastname'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            "profile_picture": forms.HiddenInput()
        }


class SellerProfileForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    bank_account = AccountNumberField(max_length=11, min_length=11)
    class Meta:
        model = SellerProfile
        fields = [
            'tradename',
            'firstname',
            'lastname',
            'phone_number',
            'email',
            'website',
            'city',
            'state',
            'address',
            'bank_account',
            'brand_logo'
        ]

        widgets = {
            'brand_logo': forms.HiddenInput()
        }


class UpdateSellerProfileForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    bank_account = AccountNumberField(max_length=11, min_length=11)
    class Meta:
        model = SellerProfile
        fields = [
            'tradename',
            'phone_number',
            'email',
            'website',
            'city',
            'state',
            'address',
            'bank_account',
            'brand_logo'
        ]
        widgets = {
            'brand_logo': forms.HiddenInput(),
            'phone_number': forms.TextInput(attrs={'placeholder': '+12125552368'}),
            'email': forms.TextInput(attrs={'type': 'email', 'placeholder': 'your@example.com'}),
            'website': forms.TextInput(attrs={'placeholder': 'https://www.example.com'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }


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
        labels = {
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
