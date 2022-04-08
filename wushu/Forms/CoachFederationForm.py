from django.forms import ModelForm, forms
from django import forms

from wushu.models import Coach


class CoachFederationForm(ModelForm):
    class Meta:
        model = Coach

        fields = ('federation',)

        labels = {'federation': 'Federation(*)'}
        widgets = {

            'federation': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%;', 'required': 'required'}),

        }
