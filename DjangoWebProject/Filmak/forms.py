from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AuthUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")

class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ("username", "password1", "password2")