"""Vistas para el manejo de autenticación y registro de usuarios."""
from vlogs.models import Favorito
from skincare.models import FavoritoProducto
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

def login_view(request):
    """Maneja el inicio de sesión de usuarios."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    """Cierra la sesión del usuario actual."""
    logout(request)
    return redirect('inicio')

def registro_view(request):
    """Maneja el registro de nuevos usuarios y asignación de roles."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        rol = request.POST.get('rol', 'Usuario')
        if form.is_valid():
            user = form.save()
            grupo, _ = Group.objects.get_or_create(name=rol)
            user.groups.add(grupo)
            if rol == 'Admin':
                user.is_staff = True
                user.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada!')
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def perfil_view(request):
    """Muestra el perfil del usuario autenticado."""
    return render(request, 'usuarios/perfil.html')


@login_required
def perfil_view(request):
    favoritos_vlogs = Favorito.objects.filter(
        usuario=request.user
    ).select_related('post')

    favoritos_productos = FavoritoProducto.objects.filter(
        usuario=request.user
    ).select_related('producto')

    return render(request, 'usuarios/perfil.html', {
        'favoritos_vlogs': favoritos_vlogs,
        'favoritos_productos': favoritos_productos,
    })