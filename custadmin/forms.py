from django import forms
from home.models import *
from django.forms import widgets
from django.forms import DateInput
from datetime import date
class AdminClaimForm(forms.ModelForm):
    class Meta:
        model = Claims
        fields = ["user","policy_number","status","res_amt","amt","reason"]

class AdminPolicyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().strftime('%Y-%m-%d')
        self.fields['start_date'].widget.attrs.update({'type': 'date', 'min': today, 'value': today})

    class Meta:
        model = Policys
        fields = ["user","holder_name","start_date","end_date","premuim","coverage","policy_type"]
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

class AdminApprovalClaimForm(forms.ModelForm):
    class Meta:
        model = Claims
        fields = ["status"]
