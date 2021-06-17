from django import forms
from .models import ProvidersAndCustomers

class ProviderAndCustomerForm(forms.ModelForm):

    class Meta:
        model = ProvidersAndCustomers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['direction'].widget.attrs.update({
            'rows': '3',
        })
        self.fields['description'].widget.attrs.update({
            'rows': '3',
        })