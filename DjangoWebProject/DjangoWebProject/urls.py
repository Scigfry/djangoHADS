from django.urls import path
from Filmak import views

urlpatterns = [
    path('', views.home, name='base'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ver_pelis/', views.ver_pelis, name='ver_pelis'),
    path('votar/', views.votar, name='votar'),
    path('seguidores/', views.seguidores, name='seguidores'),
]