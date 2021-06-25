from django import forms
from .models import Model


class ModelForm(forms.ModelForm):

    def clean_name(self):
        try:
            model = Model.objects.get(
                name__iexact=self.cleaned_data['name'].strip())
            if not self.instance.pk:
                raise forms.ValidationError('Este modelo ya existe')
            elif self.instance.pk != model.pk:
                raise forms.ValidationError(
                    'Cambio no permitido el modelo ya existe')
        except Model.DoesNotExist:
            pass
        return self.cleaned_data['name']

    class Meta:
        model = Model
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
        })
