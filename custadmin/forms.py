from django import forms
from home.models import *
from django.forms import widgets

class AdminClaimForm(forms.ModelForm):
    class Meta:
        model = Claims
        fields = ["user","policy_number","status","res_amt","amt","reason"]

class AdminPolicyForm(forms.ModelForm):
    class Meta:
        model = Policys
        fields = ["user","holder_name","start_date","end_date","premuim","coverage","policy_type"]