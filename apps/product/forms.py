from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        labels = {'name': 'Nombre'}
        help_text = {'name': 'Nombre del producto'}
        error_messages = {'name': {'required': 'El campo nombre es requerido'}}

    def clean(self):
        try:
            product = Product.objects.get(name=self.cleaned_data['name'].strip())
            if not self.instance.pk:
                raise forms.ValidationError('Este producto ya existe')
            elif self.instance.pk != product.pk:
                raise forms.ValidationError(
                    'Cambio no permitido el producto ya existe')
        except Product.DoesNotExist:
            pass
        return self.cleaned_data
