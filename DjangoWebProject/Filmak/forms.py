from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Validar credenciales de inicio de sesión
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")

        return cleaned_data

class RegistroForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password", "password_confirm")

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        # Validar coincidencia de contraseñas
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        # Establecer contraseña para el usuario
        user.set_password(password)
        if commit:
            user.save()

        return user
