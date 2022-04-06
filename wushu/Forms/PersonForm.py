from django import forms
from django.forms import ModelForm

from wushu.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'pasaport', 'profileImage','birthDate', 'gender','pasaportImage',)
        labels = {'pasaport': 'Pasaport number (*)', 'gender': 'Gender','birthDate':'Birth Date(*)', }

        widgets = {


            'pasaport': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

        }

    def clean_tc(self):

        data = self.cleaned_data['tc']
        print(self.instance)
        if self.instance is None:
            if Person.objects.filter(tc=data).exists():
                raise forms.ValidationError("This tc already used")
            return data
        else:
            return data
