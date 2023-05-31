from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistroForm
from .models import Filma

def home(request):
    return render(request, 'base.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Lógica para procesar el formulario de registro
            form.save()
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                auth_login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def ver_pelis(request):
    films = Filma.objects.all()
    return render(request, 'ver_pelis.html', {'films': films})

@login_required
def votar(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de votación
        return redirect('home')
    return render(request, 'votar.html')

@login_required
def seguidores(request):
    # Lógica para obtener la información de los seguidores y las películas votadas
    return render(request, 'seguidores.html')
