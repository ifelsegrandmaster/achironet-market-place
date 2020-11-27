from django import forms
from .models import Order, ShippingInformation

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


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class ShippingInformationForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    class Meta:
        model = ShippingInformation
        fields = [
            'fullname',
            'phone_number',
            'email',
            'street_address',
            'apartment',
            'state',
            'city',
        ]
