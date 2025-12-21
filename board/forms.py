from django import forms
from .models import Com2,Com1_board

class Com2Form(forms.ModelForm):
    class Meta:
        model = Com2
        fields = ['title', 'description', 'upload']


class Com1Form(forms.ModelForm):
    class Meta:
        model = Com1_board
        fields = ['title', 'description', 'upload']