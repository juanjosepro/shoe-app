from django import forms
from .models import Sizes


class SizesForm(forms.ModelForm):

    class Meta:
        model = Sizes
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['size'].widget.attrs.update({
            'placeholder':'38-42',
        })