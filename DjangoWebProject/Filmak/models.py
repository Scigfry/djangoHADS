from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class AuthUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

class Filma(models.Model):
    izenburua = models.CharField(max_length=100)
    zuzendaria = models.CharField(max_length=60)
    urtea = models.IntegerField()
    generoa = models.CharField(max_length=2)
    sinopsia = models.CharField(max_length=500)
    bozkak = models.IntegerField()

class Erabiltzailea(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

class FilmaBozkatzailea(models.Model):
    erabiltzailea = models.ForeignKey(Erabiltzailea, on_delete=models.CASCADE)

class GogokoFilmak(models.Model):
    filmak_filma = models.ForeignKey(Filma, on_delete=models.CASCADE)
    filma_bozkatzailea = models.ForeignKey(FilmaBozkatzailea, on_delete=models.CASCADE)