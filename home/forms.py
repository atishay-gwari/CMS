from django import forms
from .models import *
from django.forms import widgets


class ClaimForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.fields['policy_number'] = forms.ModelChoiceField(
            queryset=Policys.objects.filter(user=user).values_list('policy_number', flat=True),
            empty_label=None,
            widget=forms.Select(attrs={'class': 'form-select'})
        )

    class Meta:
        model = Claims
        fields = ['policy_number', 'amt', 'reason']