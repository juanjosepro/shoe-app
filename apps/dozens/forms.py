from django import forms
from .models import Dozen

class DozenForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))

    class Meta:
        model = Dozen
        fields = '__all__'