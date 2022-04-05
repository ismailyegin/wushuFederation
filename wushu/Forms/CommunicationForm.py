from django import forms
from django.forms import ModelForm

from wushu.models import Communication


class CommunicationForm(ModelForm):
    class Meta:
        model = Communication

        fields = ( 'city', 'country')
        labels = {'country': 'Country(*)'}
        widgets = {

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),

        }
