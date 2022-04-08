from django.forms import ModelForm, forms
from django import forms

from wushu.models import Officer


class OfficerFederationForm(ModelForm):
    class Meta:
        model = Officer

        fields = ('federation',)

        labels = {'federation': 'Federation(*)'}
        widgets = {

            'federation': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%;', 'required': 'required'}),

        }
