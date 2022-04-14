from django import forms
from django.forms import ModelForm

from wushu.models.SandaWeightCategory import SandaWeightCategory


class SandaWeightCategoryForm(ModelForm):
    class Meta:
        model = SandaWeightCategory
        fields = ('categoryName', 'ageGroup', 'gender')
        labels = {'categoryName': 'Category Name', 'ageGroup': 'Age Group', 'gender': 'Gender'}
        widgets = {
            'categoryName': forms.TextInput(
                attrs={'class': 'form-control', }),
            'gender': forms.TextInput(
                attrs={'class': 'form-control', }),
            'ageGroup': forms.TextInput(
                attrs={'class': 'form-control '}),

        }
