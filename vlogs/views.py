from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post

def inicio(request):
    posts_recientes = Post.objects.all().order_by('-fecha')[:3]
    return render(request, 'inicio.html', {'posts': posts_recientes})

def lista_vlogs(request):
    destino = request.GET.get('destino', '')
    posts = Post.objects.all().order_by('-fecha')
    if destino:
        posts = posts.filter(destino=destino)
    return render(request, 'vlogs/lista.html', {'posts': posts, 'destino': destino})

def detalle_vlog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'vlogs/detalle.html', {'post': post})

@login_required
def crear_vlog(request):
    if not request.user.is_staff:
        return redirect('inicio')
    if request.method == 'POST':
        titulo      = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        destino     = request.POST.get('destino', '')
        imagen      = request.FILES.get('imagen')
        if titulo and descripcion and destino:
            post = Post.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                destino=destino,
                autor=request.user,
            )
            if imagen:
                post.imagen = imagen
                post.save()
            messages.success(request, 'Vlog publicado correctamente.')
            return redirect('detalle_vlog', pk=post.pk)
    return render(request, 'vlogs/crear.html')

@login_required
def editar_vlog(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.titulo      = request.POST.get('titulo', post.titulo).strip()
        post.descripcion = request.POST.get('descripcion', post.descripcion).strip()
        post.destino     = request.POST.get('destino', post.destino)
        if request.FILES.get('imagen'):
            post.imagen = request.FILES['imagen']
        post.save()
        messages.success(request, 'Vlog actualizado.')
        return redirect('detalle_vlog', pk=post.pk)
    return render(request, 'vlogs/editar.html', {'post': post})

@login_required
def eliminar_vlog(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Vlog eliminado.')
        return redirect('lista_vlogs')
    return render(request, 'vlogs/eliminar.html', {'post': post})

@login_required
def detalle_vlog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    ya_es_favorito = False
    if request.user.is_authenticated:
        from .models import Favorito
        ya_es_favorito = Favorito.objects.filter(
            usuario=request.user, post=post
        ).exists()
    comentarios = post.comentarios.all().order_by('-fecha')
    return render(request, 'vlogs/detalle.html', {
        'post': post,
        'ya_es_favorito': ya_es_favorito,
        'comentarios': comentarios,
    })
@login_required
def toggle_favorito_vlog(request, pk):
    from .models import Favorito
    post = get_object_or_404(Post, pk=pk)
    favorito = Favorito.objects.filter(usuario=request.user, post=post)
    if favorito.exists():
        favorito.delete()
        messages.success(request, 'Eliminado de favoritos')
    else:
        Favorito.objects.create(usuario=request.user, post=post)
        messages.success(request, 'Guardado en favoritos')
    return redirect('detalle_vlog', pk=pk)


@login_required
def agregar_comentario(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            from .models import Comentario
            Comentario.objects.create(
                post=post,
                usuario=request.user,
                contenido=contenido
            )
            messages.success(request, 'Comentario publicado.')
    return redirect('detalle_vlog', pk=pk)