from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  # 'is_active',
                  'email', )
        labels = {'first_name': 'Name(*)', 'last_name': 'Surname(*)', 'email': 'Email(*)',
                  # 'is_active': 'Is Active'
                  }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'email': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            # 'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper', 'required': 'required'}),

        }

    def clean_email(self):

        data = self.cleaned_data['email']
        print(self.instance)
        if  self.instance.id is None:
            if User.objects.filter(email=data).exists():
                raise forms.ValidationError("Bu email başka bir kullanıcı tarafından kullanılmaktadır.")
            return data
        else:
            return data

    # def save(self, commit=False):
    #     self.first_name=self.cleaned_data['first_name'].upper()
    #     self.last_name=self.cleaned_data['last_name'].upper()
    #     print(self.first_name)
    #     # self.first_name = self.first_name.upper()
    #     # self.last_name = self.last_name.upper()
    #     return ModelForm.save(self, commit=False)




    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
