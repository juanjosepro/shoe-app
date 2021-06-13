from django import forms
from django.forms import ValidationError
from .models import ProvidersAndCustomers

class ProviderAndCustomerForm(forms.ModelForm):
    
    direction = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    
    class Meta:
        model = ProvidersAndCustomers
        fields = '__all__'
