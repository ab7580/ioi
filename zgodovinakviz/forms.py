from django import forms

from .models import Vprasanje
from .models import Odgovor

class VprasanjeForm(forms.ModelForm):

    class Meta:
        model = Vprasanje
        fields = ('vprasanje', 'pravilen_odgovor', 'napacen_odgovor_1', 'napacen_odgovor_2', 'namig', 'slika')
        widgets = {
            'vprasanje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vprašanje'}),
            'pravilen_odgovor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pravilni odgovor'}),
            'napacen_odgovor_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prvi napačni odgovor'}),
            'napacen_odgovor_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drugi napačni odgovor'}),
            'namig': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Namig'}),
            'slika': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL slike'})
        }

class VprasanjeEditForm(forms.ModelForm):

    class Meta:
        model = Vprasanje
        fields = ('vprasanje', 'pravilen_odgovor', 'napacen_odgovor_1', 'napacen_odgovor_2', 'namig', 'slika')
        widgets = {
            'vprasanje': forms.TextInput(attrs={'class': 'form-control'}),
            'pravilen_odgovor': forms.TextInput(attrs={'class': 'form-control'}),
            'napacen_odgovor_1': forms.TextInput(attrs={'class': 'form-control'}),
            'napacen_odgovor_2': forms.TextInput(attrs={'class': 'form-control'}),
            'namig': forms.TextInput(attrs={'class': 'form-control'}),
            'slika': forms.TextInput(attrs={'class': 'form-control'})
        }

class OdgovorForm(forms.ModelForm):

    class Meta:
        model = Odgovor
        fields = ('izbran_odgovor',)