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

        self.fields['provider'].widget.attrs.update({
            'class':'selectpicker',
            'data-style': 'btn btn-link'
        })
        self.fields['amount'].widget.attrs.update({
            'min':'1',
            'pattern':'^[0-9]+',
        })
        self.fields['color'].widget.attrs.update({
            'class':'selectpicker',
            'data-style': 'btn btn-link'
        })
        self.fields['price'].widget.attrs.update({
            'autocomplete': 'off',
            'min':'1',
            'pattern':'^[0-9]+',
        })
        self.fields['note'].widget.attrs.update({
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
            'readonly': True,
            'class': 'form-control text-uppercase'
        })
        self.fields['provider'].widget.attrs.update({
            'readonly': True,
            'class': 'text-uppercase',
        })
        self.fields['amount'].widget.attrs.update({
            'readonly': True,
        })
        self.fields['stock'].widget.attrs.update({
            'type':'number',
            'min':'0',
            'pattern':'^[0-9]+',
        })
        self.fields['color'].widget.attrs.update({
            'readonly': True,
            'class': 'text-uppercase'
        })
        self.fields['type'].widget.attrs.update({
            'readonly': True,
            'class': 'text-uppercase'
        })
        self.fields['price'].widget.attrs.update({
            'readonly': True,
            'autocomplete': 'off'
        })
        self.fields['note'].widget.attrs.update({
            'readonly': True,
            'rows':'3',
        })

class ReadonlyForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['stock'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['material'].widget.attrs.update({
            'disabled': True,
            'class': 'form-control text-uppercase'
        })
        self.fields['provider'].widget.attrs.update({
            'disabled': True,
            'class': 'text-uppercase',
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
            'class': 'text-uppercase'
        })
        self.fields['type'].widget.attrs.update({
            'disabled': True,
            'class': 'text-uppercase'
        })
        self.fields['price'].widget.attrs.update({
            'disabled': True,
        })
        self.fields['note'].widget.attrs.update({
            'disabled': True,
            'rows':'3',
        })