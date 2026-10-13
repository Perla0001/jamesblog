from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Nota

@login_required
def estudio_view(request):
    return render(request, 'coreano/estudio.html')

@login_required
def lista_notas(request):
    notas = Nota.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'coreano/notas.html', {'notas': notas})

@login_required
def crear_nota(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        if titulo and contenido:
            Nota.objects.create(usuario=request.user, titulo=titulo, contenido=contenido)
        return redirect('lista_notas')
    return render(request, 'coreano/crear_nota.html')

@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk, usuario=request.user)
    nota.delete()
    return redirect('lista_notas')