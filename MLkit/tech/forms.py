import csv
import io

from django import forms
from django.core.validators import FileExtensionValidator

from .models import selectedData

class UploadFileForm(forms.ModelForm):

    class Meta:
        model  = selectedData 
        fields = ('title', 'upload' )
        
