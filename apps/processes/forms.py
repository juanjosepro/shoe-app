from django import forms
""" from .models import DozensOfAparadores, DozensOfArmadores, DozensOfRematadoras


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
        }) """