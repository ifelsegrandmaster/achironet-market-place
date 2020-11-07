from django import forms
from .models import Order, ShippingInformation

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class ShippingInformationForm(forms.ModelForm):
    class Meta:
        model = ShippingInformation
        fields = [
            'fullname',
            'phone_number',
            'email',
            'street_address',
            'apartment',
            'country',
            'state',
            'city',
            'postal_code'
        ]