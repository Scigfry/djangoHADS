from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import LoginForm, RegistroForm
from .models import AuthUser, Filma

def home(request):
    request.session.setdefault('columna_izquierda_template', 'columna_izquierda.html')
    columna_izquierda_template = request.session['columna_izquierda_template']
    return render(request, 'base.html', {'columna_izquierda_template': columna_izquierda_template})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')  # Redirigir a la página de inicio de sesión después del registro exitoso
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = AuthUser.objects.get(username=username)
                if user.password == password:
                    auth_login(request, user)
                    request.session['columna_izquierda_template'] = 'columna_izquierda_logged.html'
                    return render(request, 'base.html')
                else:
                    form.add_error('password', 'Contraseña incorrecta')  # Agregar error al formulario
            except AuthUser.DoesNotExist:
                form.add_error('username', 'El usuario no existe')  # Agregar error al formulario
            
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    request.session.setdefault('columna_izquierda_template', 'columna_izquierda.html')
    columna_izquierda_template = request.session['columna_izquierda_template']
    request.session['columna_izquierda_template'] = 'columna_izquierda.html'
    return render(request, 'base.html', {'columna_izquierda_template': columna_izquierda_template})

def ver_pelis(request):
    filmak_list = Filma.objects.all()
    paginator = Paginator(filmak_list, 5)  # Muestra 10 películas por página
    page_number = request.GET.get('page')
    filmak = paginator.get_page(page_number)
    return render(request, 'ver_pelis.html', {'filmak': filmak})

def votar(request):
    if request.method == 'POST':
        # Lógica para procesar el formulario de votación
        return redirect('home')
    return render(request, 'votar.html')

def seguidores(request):
    # Lógica para obtener la información de los seguidores y las películas votadas
    return render(request, 'seguidores.html')