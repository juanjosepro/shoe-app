from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):

    amount = forms.CharField(widget=forms.TextInput(attrs={
        'type':'number',
        'class':'form-control',
        'min':'0',
        'pattern':'^[0-9]+',
    }))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={
        'type':'number',
        'class':'form-control',
        'min':'0',
        'pattern':'^[0-9]+',
    }))
    note = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'3'}))

    class Meta:
        model = Inventory
        fields = '__all__'