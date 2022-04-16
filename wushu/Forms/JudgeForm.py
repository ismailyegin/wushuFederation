from django import forms
from django.forms import ModelForm

from wushu.models import Judge


class JudgeForm(ModelForm):
    is_national = forms.BooleanField(required=False)
    class Meta:
        model = Judge

        fields = ('category', 'is_national', )

        labels = {'category': 'Role(*)', 'is_national': 'Do you have a national judging certificate?', }
        widgets = {

            'category': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;', 'required': 'required','onchange':'categoryJudge()'}),

        }
