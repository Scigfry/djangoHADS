from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AuthUser, Filma

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class RegistroForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = AuthUser
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

class AnadirFilmForm(forms.ModelForm):
    izenburua = forms.CharField(label='Izenburua')
    zuzendaria = forms.CharField(label='Zuzendaria')
    urtea = forms.IntegerField(label='Urtea', min_value = 1)
    sinopsia = forms.CharField(label='Sinopsia')
    bozkak = forms.IntegerField(label='Bozkak', initial=0, disabled=True)
    generoa = forms.ChoiceField(label='Generoa', choices=[('AC', 'Acción'), ('AV', 'Aventura'), ('CO', 'Comedia'), ('DR', 'Drama'), ('TE', 'Terror')])

    class Meta:
        model = Filma
        fields = ('izenburua', 'zuzendaria', 'urtea', 'sinopsia', 'bozkak', 'generoa')

