from django import forms
from django.forms import ModelForm

from wushu.models.TaoluCategory import TaoluCategory


class TaoluCategoryForm(ModelForm):
    class Meta:
        model = TaoluCategory
        fields = ('categoryName', 'isDuilian','explanation')
        labels = {'categoryName': 'Tanımı', 'isDuilian': 'Duilian mı?','explanation':'Açıklama'}
        widgets = {
            'categoryName': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'isDuilian': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),
            'explanation': forms.TextInput(
                attrs={'class': 'form-control '}),
        }
