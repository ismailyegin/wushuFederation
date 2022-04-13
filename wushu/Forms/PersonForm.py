from django import forms
from django.forms import ModelForm

from wushu.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person

        fields = (
            'name', 'surName', 'pasaport', 'profileImage', 'birthDate', 'gender', 'pasaportImage', 'country')
        labels = {'name': 'Name (*)', 'surName': 'Surname (*)', 'pasaport': 'Passport Number (*)', 'gender': 'Gender',
                  'birthDate': 'Date of birth (*)', 'country': 'Country (*)'}

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'surName': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'pasaport': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'birthDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask2013', 'autocomplete': 'on',
                       'required': 'required'}),

            'gender': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'country': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%;', 'required': 'required'}),

            'profileImage': forms.FileInput(attrs={'id': 'id_profileImage', 'name': 'profileImage',
                                                   'onchange': 'previewImage()', }),

            'pasaportImage': forms.FileInput(attrs={'id': 'id_passportImage', 'name': 'passportImage',
                                                   'onchange': 'previewImage2()', }),

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
