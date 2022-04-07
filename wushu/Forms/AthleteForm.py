from django.forms import ModelForm, forms
from django import forms

from wushu.models import Athlete


class AthleteForm(ModelForm):
    class Meta:
        model = Athlete

        fields = ('ekg', 'eeg',)

