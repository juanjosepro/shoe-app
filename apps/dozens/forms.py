from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Dozen, DozensOfCortadores
from .models import DozensOfAparadores, DozensOfArmadores, DozensOfRematadoras

class DozenCreateForm(forms.ModelForm):
    class Meta:
        model = Dozen
        fields = '__all__'
        labels = {'user': 'Elija al cortador de esta docena'}
        exclude = ['status', 'model', 'size']
        """ widgets = {
            'model': AutocompleteSelect(
                Dozen._meta.get_field('model').remote_field,
                admin.site,
                #attrs={'placeholder': 'Seleccione un modelo'}
            )
        } """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #self.fields['size'].queryset = User.objects.filter(groups__name='cortadores')
        self.fields['material'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
        })


class DozenUpdateForm(forms.ModelForm):
    class Meta:
        model = Dozen
        exclude = ['code']
        fields = '__all__'
        labels = {
            'status': 'El estado actual de esta docena es'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['material'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['note'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
        })


class DozensOfCortadoresForm(forms.ModelForm):

    class Meta:
        model = DozensOfCortadores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['note'].widget.attrs.update({
            'rows': '3',
        })
class DozensOfAparadoresForm(forms.ModelForm):

    class Meta:
        model = DozensOfAparadores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['note'].widget.attrs.update({
            'rows': '3',
        })

class DozensOfArmadoresForm(forms.ModelForm):

    class Meta:
        model = DozensOfArmadores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['note'].widget.attrs.update({
            'rows': '3',
        })

class DozensOfRematadorasForm(forms.ModelForm):

    class Meta:
        model = DozensOfRematadoras
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['note'].widget.attrs.update({
            'rows': '3',
        })