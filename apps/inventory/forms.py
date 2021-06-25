from django import forms
from django.forms.widgets import HiddenInput
from .models import Inventory
from apps.providers_and_customers.models import ProvidersAndCustomers


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['material'].widget = HiddenInput()
        self.fields['stock'].widget = HiddenInput()
        self.fields['type'].widget = HiddenInput()

        self.fields['provider'].queryset = ProvidersAndCustomers.objects.filter(types='proveedor')

        self.fields['amount'].widget.attrs.update({
            'type':'number',
            'class':'form-control',
            'min':'1',
            'pattern':'^[0-9]+',
        })
        self.fields['color'].widget.attrs.update({
            'class':'form-control',
        })
        self.fields['price'].widget.attrs.update({
            'type':'number',
            'autocomplete': 'off',
            'class':'form-control',
            'min':'1',
            'pattern':'^[0-9]+',
        })
        self.fields['note'].widget.attrs.update({
            'class':'form-control',
            'rows':'3',
        })


class UpdateStockForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['stock'].widget.attrs.update({
            'autofocus': True,
        })
        self.fields['material'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['provider'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['amount'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['stock'].widget.attrs.update({
            'type':'number',
            'min':'0',
            'pattern':'^[0-9]+',
        })
        self.fields['color'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['type'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['price'].widget.attrs.update({
            'disabled': True,
            'autocomplete': 'off'
        })
        self.fields['note'].widget.attrs.update({
            'disabled': True,
            'rows':'3',
        })