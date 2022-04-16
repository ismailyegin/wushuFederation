from django import forms
from django.forms import ModelForm

from wushu.models import Judge


class JudgeForm(ModelForm):
    class Meta:
        model = Judge

        fields = ('category',)

        labels = {'category': 'Role(*)', }
        widgets = {

            'category': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;', 'required': 'required','onchange':'categoryJudge()'}),

        }
