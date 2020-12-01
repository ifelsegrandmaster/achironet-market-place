from django import forms
from shop.models import Product, Category

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class ProductFilterForm(forms.Form):
    name = forms.CharField(max_length=90, required=False)
    published = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                  widget=forms.Select(), required=False)
    available = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                widget=forms.Select(), required=False)
