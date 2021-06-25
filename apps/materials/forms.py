from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):

    def clean_name(self):
        try:
            model = Material.objects.get(
                name__iexact=self.cleaned_data['name'].strip())
            if not self.instance.pk:
                raise forms.ValidationError('Ya existe un material con este nombre')
            elif self.instance.pk != model.pk:
                raise forms.ValidationError(
                    'Cambio no permitido un material con este nombre ya existe')
        except Material.DoesNotExist:
            pass
        return self.cleaned_data['name']
    class Meta:
        model = Material
        fields = '__all__'