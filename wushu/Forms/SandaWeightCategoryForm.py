from django import forms
from django.forms import ModelForm

from wushu.models.SandaWeightCategory import SandaWeightCategory


class SandaWeightCategoryForm(ModelForm):
    class Meta:
        model = SandaWeightCategory
        fields = ('categoryName', 'isDuilian', 'explanation')
        labels = {'categoryName': 'Category Name', 'isDuilian': 'isDuilian', 'explanation': 'explanation'}
        widgets = {
            'categoryName': forms.TextInput(
                attrs={'class': 'form-control', }),
            'isDuilian': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            'explanation': forms.TextInput(
                attrs={'class': 'form-control '}),

        }
