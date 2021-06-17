from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    
    class Meta:
        model = Inventory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs.update({
            'type':'number',
            'class':'form-control',
            'min':'0',
            'pattern':'^[0-9]+',
        })
        self.fields['color'].widget.attrs.update({
            'class':'form-control',
        })
        self.fields['price'].widget.attrs.update({
            'type':'number',
            'class':'form-control',
            'min':'0',
            'pattern':'^[0-9]+',
        })
        self.fields['note'].widget.attrs.update({
            'class':'form-control',
            'rows':'3',
        })