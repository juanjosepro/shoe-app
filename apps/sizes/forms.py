from django import forms
from .models import Sizes


class SizesForm(forms.ModelForm):

    class Meta:
        model = Sizes
        fields = '__all__'