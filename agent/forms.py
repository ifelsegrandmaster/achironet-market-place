from django import forms
from .models import AgentProfile

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

class CreateAgentForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    profile_picture = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = AgentProfile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'city',
            'state',
            'address',
        ]