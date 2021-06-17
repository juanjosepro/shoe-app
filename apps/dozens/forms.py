from django import forms
from .models import Dozen

class DozenForm(forms.ModelForm):
    class Meta:
        model = Dozen
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['material'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
        })
        