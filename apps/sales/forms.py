from apps.providers_and_customers.models import ProvidersAndCustomers
from django import forms
from .models import Sales

class SalesForm(forms.ModelForm):

    class Meta:
        model = Sales
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'].queryset = ProvidersAndCustomers.objects.filter(types='cliente')

        self.fields['customer'].widget.attrs.update({
            'class':'form-control selectpicker',
            'data-style': 'btn btn-link',
        })
        self.fields['status'].widget.attrs.update({
            'class':'form-control selectpicker',
            'data-style': 'btn btn-link',
        })
        self.fields['note'].widget.attrs.update({
            'rows':'3',
            'class': 'form-control',
        })
