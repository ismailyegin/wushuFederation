from django import forms
from django.forms import ModelForm

from wushu.models.YearsSandaCategory import YearsSandaCategory



class SandaYearsCategoryForm(ModelForm):
    class Meta:
        model = YearsSandaCategory
        fields = ('categoryYear',)
        labels = {'categoryYear': 'Kategori Yaşı'}
        widgets = {
            'categoryYear': forms.TextInput(
                attrs={'class': 'form-control ',}),

        }
