from django import forms
from .models import Com2

class Com2Form(forms.ModelForm):
    class Meta:
        model = Com2
        fields = ['title', 'description', 'upload']
