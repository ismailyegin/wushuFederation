from django import forms
from django.forms import ModelForm

from wushu.models import Competition


class CompetitionSearchForm(ModelForm):



    class Meta:
        model = Competition

        fields = (
            'name',)

        labels = {'name': 'İsim',
                  }

        widgets = {


            'name': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),






        }
