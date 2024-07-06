from django import forms
from .models import FormData

class FormDataForm(forms.ModelForm):
    class Meta:
        model = FormData
        fields = '__all__'  # Use all fields from the FormData model