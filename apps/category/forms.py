from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    def clean_name(self):
        try:
            category = Category.objects.get(
                name__iexact=self.cleaned_data['name'].strip())
            if not self.instance.pk:
                raise forms.ValidationError('Esta categoría ya existe')
            elif self.instance.pk != category.pk:
                raise forms.ValidationError(
                    'Cambio no permitido, la categoría ya existe')
        except Category.DoesNotExist:
            pass
        return self.cleaned_data['name']

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({
            'rows': '3',
        })
