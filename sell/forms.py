from django import forms
from shop.models import Product, Category
from django.core.validators import ValidationError

TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)

FALSE_TRUE_CHOICES = (
    (False, 'No'),
    (True, 'Yes')
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
                ('Invalid account number: %(value)s'),
                code='invalid',
                params={'value': value},
            )


class ProductFilterForm(forms.Form):
    name = forms.CharField(max_length=90, required=False)
    published = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                  widget=forms.Select(), required=False)
    available = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                  widget=forms.Select(), required=False)


class OrderFilterForm(forms.Form):
    name = forms.CharField(max_length=90, required=False)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


class ClaimMoneyForm(forms.Form):
    bank_name = forms.CharField(max_length=90, required=True)
    account_number = AccountNumberField(
        max_length=11, min_length=11, required=True)
