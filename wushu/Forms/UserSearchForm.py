from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from wushu.models import Person


class UserSearchForm(ModelForm):

    class Meta:
        model = Person
        fields = ('name', 'surName')
        labels = {'name': 'Name', 'surName': 'Surname'}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Name', 'value': ''}),
            'surName': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': ' Surname'}),
        }
