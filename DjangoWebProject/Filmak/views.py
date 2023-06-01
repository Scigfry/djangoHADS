from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import LoginForm, RegistroForm
from .models import AuthUser, Filma, GogokoFilmak, FilmaBozkatzailea, Erabiltzailea

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
                    request.session['username'] = username
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
    request.session['username'] = ''
    return render(request, 'base.html', {'columna_izquierda_template': columna_izquierda_template})

def ver_pelis(request):
    filmak_list = Filma.objects.all()
    paginator = Paginator(filmak_list, 5)  # Muestra 10 películas por página
    page_number = request.GET.get('page')
    filmak = paginator.get_page(page_number)
    return render(request, 'ver_pelis.html', {'filmak': filmak})

def votar(request):
    filmak = Filma.objects.all()
    if request.method == 'POST':
        mensaje = "¡Voto registrado con éxito!"
        pelicula_id = request.POST.get('pelicula')
        username = request.session['username']
        user = AuthUser.objects.get(username=username)

        try:
            erabiltzailea = Erabiltzailea.objects.get(auth_user=user)
        except Erabiltzailea.DoesNotExist:
            # Si Erabiltzailea no existe, crearlo junto con FilmaBozkatzailea
            filma_bozkatzailea = FilmaBozkatzailea.objects.create(erabiltzailea_id=user.id)
            erabiltzailea = Erabiltzailea.objects.create(auth_user=user, filma_bozkatzailea=filma_bozkatzailea)

        # Verificar si el usuario ya ha votado la película
        if not GogokoFilmak.objects.filter(filma_id=pelicula_id, filma_gogokoa=erabiltzailea.filma_bozkatzailea).exists():
            filma = Filma.objects.get(id=pelicula_id)

            # Crear instancia de GogokoFilmak
            gogoko_filmak = GogokoFilmak.objects.create(filma=filma, filma_gogokoa=erabiltzailea.filma_bozkatzailea)

            # Incrementar el campo 'bozkak' de la película en uno
            filma.bozkak += 1

            # Guardar los cambios en los modelos
            gogoko_filmak.save()
            filma.save()

        else:
            mensaje = "Ya has votado esta película previamente."

        return render(request, 'votar.html', {'mensaje': mensaje, 'filmak': filmak})

    return render(request, 'votar.html', {'filmak': filmak})


def seguidores(request):
    filmak = Filma.objects.all()
    votos = GogokoFilmak.objects.select_related('filma', 'filma_gogokoa__erabiltzailea__auth_user')

    pelicula_id = None
    if 'pelicula' in request.GET:
        pelicula_id = request.GET['pelicula']
        if pelicula_id:
            pelicula_id = int(pelicula_id)

    context = {
        'filmak': filmak,
        'votos': votos,
        'pelicula_id': pelicula_id,
    }

    return render(request, 'seguidores.html', context)