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
    description = forms.CharField(min_length=50, max_length=500, widget=forms.Textarea())
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
