from django import forms
from django.forms import ModelForm

from wushu.models.YearsTaoluCategory import YearsTaoluCategory


class YearsTaoluCategoryForm(ModelForm):
    class Meta:
        model = YearsTaoluCategory
        fields = ('categoryYear',)
        labels = {'categoryYear': 'Kategori Yaşı'}
        widgets = {
            'categoryYear': forms.TextInput(
                attrs={'class': 'form-control ',}),

        }
