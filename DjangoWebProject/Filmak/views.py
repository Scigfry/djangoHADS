
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Filma
def home(request):
    return render(request, 'Filmak/plantillas/base.html')

def registro(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de registro
        return redirect('home')
    return render(request, 'Filmak/plantillas/registro.html')

def login(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de inicio de sesión
        return redirect('home')
    return render(request, 'Filmak/plantillas/login.html')

def logout(request):
    # Lógica para cerrar la sesión del usuario
    return redirect('home')

@login_required
def ver_pelis(request):
    films = Filma.objects.all()
    return render(request, 'Filmak/plantillas/ver_pelis.html', {'films': films})

@login_required
def votar(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de votación
        return redirect('home')
    return render(request, 'Filmak/plantillas/votar.html')

@login_required
def seguidores(request):
    # Lógica para obtener la información de los seguidores y las películas votadas
    return render(request, 'Filmak/plantillas/seguidores.html')