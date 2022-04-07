from django import forms
from django.forms import ModelForm

from wushu.models import Competition


class DisabledCompetitionForm(ModelForm):
    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate', 'location', 'branch', 'status', 'type', 'subBranch')

        labels = {'name': 'Name', 'startDate': 'Starting Date', 'finishDate': 'End Date',
                  'location': 'Location', 'branch': 'Branch', 'status': 'Registration Status', 'type': 'Type',
                  'subBranch': 'Sub-Branch'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'disabled': 'disabled'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'disabled': 'disabled'}),

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; ', 'disabled': 'disabled'}),

            'subBranch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; ', 'disabled': 'disabled'}),

            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'disabled': 'disabled'}),

            'location': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'disabled': 'disabled'}),

            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required', 'disabled': 'disabled'}),

            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required', 'disabled': 'disabled'}),

        }
