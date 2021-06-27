from django import forms
from django.forms.widgets import HiddenInput
from .models import ProvidersAndCustomers


class ProviderAndCustomerCreateForm(forms.ModelForm):

    class Meta:
        model = ProvidersAndCustomers
        fields = '__all__'
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['types'].widget.attrs.update({
            'class': 'selectpicker',
            'data-style': 'btn btn-link',
        })
        self.fields['direction'].widget.attrs.update({
            'rows': '3',
        })
        self.fields['description'].widget.attrs.update({
            'rows': '3',
        })


class ProviderAndCustomerUpdateForm(forms.ModelForm):

    class Meta:
        model = ProvidersAndCustomers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['types'].widget = HiddenInput()

        self.fields['status'].widget.attrs.update({
            'class': 'selectpicker',
            'data-style': 'btn btn-link',
        })
        self.fields['direction'].widget.attrs.update({
            'rows': '3',
        })
        self.fields['description'].widget.attrs.update({
            'rows': '3',
        })