from django import forms
from django.core.exceptions import ValidationError
from .models import Com2, Com1_board


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            if not data and self.required:
                raise ValidationError(self.error_messages['required'])

            return [
                super(MultipleFileField, self).clean(item, initial)
                for item in data
            ]

        if data in self.empty_values:
            if self.required:
                self.validate(data)
            return []

        return [super(MultipleFileField, self).clean(data, initial)]


class Com2Form(forms.ModelForm):
    files = MultipleFileField(
        label='파일 선택',
        required=True
    )

    class Meta:
        model = Com2
        fields = ['title', 'description']


class Com1Form(forms.ModelForm):
    files = MultipleFileField(
        label='파일 선택',
        required=True
    )

    class Meta:
        model = Com1_board
        fields = ['title', 'description']