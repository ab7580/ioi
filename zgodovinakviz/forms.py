from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Vprasanje, Odgovor, Slika

class VprasanjeForm(forms.ModelForm):

    class Meta:
        model = Vprasanje
        fields = ('vprasanje', 'pravilen_odgovor', 'napacen_odgovor_1', 'napacen_odgovor_2', 'namig')
        widgets = {
            'vprasanje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vprašanje', 'required': True}),
            'pravilen_odgovor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pravilni odgovor', 'required': True}),
            'napacen_odgovor_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prvi napačni odgovor', 'required': True}),
            'napacen_odgovor_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drugi napačni odgovor', 'required': True}),
            'namig': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Namig', 'required': True})
        }

class VprasanjeEditForm(forms.ModelForm):

    class Meta:
        model = Vprasanje
        fields = ('vprasanje', 'pravilen_odgovor', 'napacen_odgovor_1', 'napacen_odgovor_2', 'namig')
        widgets = {
            'vprasanje': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'pravilen_odgovor': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'napacen_odgovor_1': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'napacen_odgovor_2': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'namig': forms.TextInput(attrs={'class': 'form-control', 'required': True})
        }

class OdgovorForm(forms.ModelForm):

    class Meta:
        model = Odgovor
        fields = ('izbran_odgovor',)


class RegistracijaForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistracijaForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Uporabniško ime'
        self.fields['username'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Elektronski naslov'
        self.fields['email'].widget.attrs['required'] = True
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Geslo'
        self.fields['password1'].widget.attrs['required'] = True
        self.fields['password1'].widget.attrs['id'] = 'password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Potrdi geslo'
        self.fields['password2'].widget.attrs['required'] = True
        self.fields['password2'].widget.attrs['id'] = 'confirmPassword'
        self.fields['password2'].widget.attrs['oninput'] = 'validate_pw2(this)'

    def save(self, commit=True):
        user = super(RegistracijaForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class VpisForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(VpisForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Uporabniško ime'
        self.fields['username'].widget.attrs['required'] = True
        self.fields['username'].widget.attrs['id'] = 'inputUsername'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Geslo'
        self.fields['password'].widget.attrs['required'] = True
        self.fields['password'].widget.attrs['id'] = 'inputPassword'

class SlikaForm(forms.ModelForm):

    class Meta:
        model = Slika
        fields = ('slika',)

    def __init__(self, *args, **kwargs):
        super(SlikaForm, self).__init__(*args, **kwargs)

        self.fields['slika'].widget.attrs['class'] = 'custom-file-input'
        self.fields['slika'].widget.attrs['id'] = 'upload'
        self.fields['slika'].widget.attrs['onchange'] = 'readURL(this);'