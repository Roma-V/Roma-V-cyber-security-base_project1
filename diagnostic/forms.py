from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Diagnose, Record

class DiagnoseRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['diagnose',]

    def clean_diagnose(self):
        diagnose = self.cleaned_data['diagnose']

        # Check if a date is not in the past.
        try:
            Diagnose.objects.get(name=diagnose)
        except:
            raise ValidationError(_('Diagnose not found'))

        # Remember to always return the cleaned data.
        return diagnose

class NewRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'symptoms',]