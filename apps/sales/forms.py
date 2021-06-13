from django import forms
from .models import Sales

class SalesForm(forms.ModelForm):

    class Meta:
        model = Sales
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].widget.attrs.update({
            'class':'form-control',
        })
        self.fields['status'].widget.attrs.update({
            'class':'form-control',
        })
        self.fields['note'].widget.attrs.update({
            'rows':'3',
            'class': 'form-control',
        })
