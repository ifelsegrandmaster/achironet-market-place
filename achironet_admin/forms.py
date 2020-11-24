from django import forms

# create all your forms here


class RequestReviewForm(forms.Form):
    group_id = forms.IntegerField()
