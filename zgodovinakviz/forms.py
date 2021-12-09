from django import forms

from .models import Vprasanje
from .models import Odgovor

class VprasanjeForm(forms.ModelForm):

    class Meta:
        model = Vprasanje
        fields = ('vprasanje', 'pravilen_odgovor', 'napacen_odgovor_1', 'napacen_odgovor_2', 'namig', 'slika')

class OdgovorForm(forms.ModelForm):

    class Meta:
        model = Odgovor
        fields = ('izbran_odgovor',)