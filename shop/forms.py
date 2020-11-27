from .models import OverView, Product
from django import forms
from django_summernote.widgets import SummernoteWidget


class OverViewForm(forms.ModelForm):

    class Meta:
        fields = ["description"]
        model = OverView
        widgets = {
            'description': SummernoteWidget()
        }


class SpecificationForm(forms.Form):
    attributes = forms.CharField(widget=forms.HiddenInput())


class ProductForm(forms.ModelForm):
    description = forms.CharField(
        min_length=50, max_length=500, widget=forms.Textarea())

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'image',
            'description',
            'price',
            'stock'
        ]


class ContactForm(forms.Form):
    name = forms.CharField(max_length=90)
    phone_number = forms.CharField(max_length=14, required=True)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        max_length=4000, required=True, widget=forms.Textarea())


class ApprovalForm(forms.Form):
    product_id = forms.IntegerField()
    message_text = forms.CharField(max_length=500, required=False)

class SearchForm(forms.Form):
    q = forms.CharField(max_length=90)
