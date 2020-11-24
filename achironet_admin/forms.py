from django import forms
from .models import EmailNewsletter
from django_summernote.widgets import SummernoteWidget
# create all your forms here


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
