from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AuthUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")

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