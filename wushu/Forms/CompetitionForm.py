from django import forms
from django.forms import ModelForm

from wushu.models import  Competition


class CompetitionForm(ModelForm):



    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate', 'location',
            'branch', 'status','type','subBranch',
            'registerStartDate','registerFinishDate')

        labels = {'name': 'Name', 'startDate': 'Starting Date', 'finishDate': 'End Date',
                  'location': 'Location', 'branch': 'Branch',
                  'status':'Registration Status','type':'Type','subBranch':'Sub-Branch',
                  'registerStartDate': 'Pre-Registration Start Date',
                  'registerFinishDate': 'Pre-Registration End Date',
                  }

        widgets = {
            'registerStartDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true',}),
            'registerFinishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6',  'autocomplete': 'on',
                       'onkeydown': 'return true', }),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'subBranch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'name': forms.TextInput(attrs={'class': 'form-control',}),

            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),



        }
