from django import forms
from django.forms import ValidationError
from .models import Model

class ModelForm(forms.ModelForm):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'type':'number', 'class':'form-control'}))

    def clean_name(self):
        name = self.cleaned_data['name']
        exists = Model.objects.filter(name__iexact = name).exists()

        if exists:
            raise ValidationError('Este nombre ya existe!')
        
        return name

    
    class Meta:
        model = Model
        fields = '__all__'
