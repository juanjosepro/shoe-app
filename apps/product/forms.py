from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'
        labels = {'name': 'Nombre'}
        help_text = {'name': 'Nombre del producto'}
        error_messages = {'name': {'required': 'El campo nombre es requerido'}}
        #widget = {'name': forms.TextInput(attrs={'class': 'test', 'placeolder': 'Nombre'})}
