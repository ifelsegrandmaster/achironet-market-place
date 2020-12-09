from django import forms
from .models import EmailNewsletter
from django_summernote.widgets import SummernoteWidget
# create all your forms here


TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class RequestReviewForm(forms.Form):
    group_id = forms.IntegerField()


class ModerateTestmonialForm(forms.Form):
    testmonial_id = forms.IntegerField()


class EmailNewsletterForm(forms.ModelForm):
    class Meta:
        model = EmailNewsletter
        fields = [
            'subject',
            'message'
        ]
        widgets = {
            'message': SummernoteWidget()
        }


class DeleteEmailNewsletterForm(forms.Form):
    email_newsletter_id = forms.IntegerField()


class OrderFilterForm(forms.Form):
    name = forms.CharField(max_length=90, required=False)
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'autocomplete': 'off'}),
        required=False
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'autocomplete': 'off'}),
        required=False
    )
    paid = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                             widget=forms.Select(), required=False)


class SellerFilterForm(forms.Form):
    firstname = forms.CharField(max_length=45, required=False)
    lastname = forms.CharField(max_length=45, required=False)


class CustomerFilterForm(forms.Form):
    firstname = forms.CharField(max_length=45, required=False)
    lastname = forms.CharField(max_length=45, required=False)

class ChangeItemForm(forms.Form):
    item_id = forms.IntegerField()