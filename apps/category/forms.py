from django import forms
from django.forms import ValidationError
from .models import Category

class CategoryForm(forms.ModelForm):

    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))

    #no funciona para actualziar porque ya existe este mismo
    """ def clean_name(self):
        name = self.cleaned_data['name']
        exists = Category.objects.filter(name__iexact = name).exists()

        if exists:
            raise ValidationError('Este nombre ya existe!')
        
        return name """

    class Meta:
        model = Category
        fields = '__all__'