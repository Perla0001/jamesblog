from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto

def lista_productos(request):
    categoria = request.GET.get('categoria', '')
    productos = Producto.objects.all()
    if categoria:
        productos = productos.filter(categoria=categoria)
    return render(request, 'skincare/lista.html', {'productos': productos, 'categoria': categoria})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'skincare/detalle.html', {'producto': producto})

@login_required
def crear_producto(request):
    if not request.user.is_staff:
        return redirect('inicio')
    if request.method == 'POST':
        nombre      = request.POST.get('nombre', '').strip()
        marca       = request.POST.get('marca', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        categoria   = request.POST.get('categoria', '')
        guia_latam  = request.POST.get('guia_latam', '')
        guia_europa = request.POST.get('guia_europa', '')
        imagen      = request.FILES.get('imagen')
        if nombre and marca and descripcion and categoria:
            p = Producto.objects.create(
                nombre=nombre, marca=marca, descripcion=descripcion,
                categoria=categoria, guia_latam=guia_latam, guia_europa=guia_europa,
            )
            if imagen:
                p.imagen = imagen
                p.save()
            messages.success(request, 'Producto publicado.')
            return redirect('detalle_producto', pk=p.pk)
    categorias = [('hidratante','Hidratante'),('protector','Protector Solar'),
                  ('serum','Sérum'),('limpiador','Limpiador'),('otro','Otro')]
    return render(request, 'skincare/crear.html', {'categorias': categorias})

@login_required
def editar_producto(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.nombre      = request.POST.get('nombre', producto.nombre).strip()
        producto.marca       = request.POST.get('marca', producto.marca).strip()
        producto.descripcion = request.POST.get('descripcion', producto.descripcion).strip()
        producto.categoria   = request.POST.get('categoria', producto.categoria)
        producto.guia_latam  = request.POST.get('guia_latam', producto.guia_latam)
        producto.guia_europa = request.POST.get('guia_europa', producto.guia_europa)
        if request.FILES.get('imagen'):
            producto.imagen = request.FILES['imagen']
        producto.save()
        messages.success(request, 'Producto actualizado.')
        return redirect('detalle_producto', pk=producto.pk)
    categorias = [('hidratante','Hidratante'),('protector','Protector Solar'),
                  ('serum','Sérum'),('limpiador','Limpiador'),('otro','Otro')]
    return render(request, 'skincare/editar.html', {'producto': producto, 'categorias': categorias})

@login_required
def eliminar_producto(request, pk):
    if not request.user.is_staff:
        return redirect('inicio')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('lista_productos')
    return render(request, 'skincare/eliminar.html', {'producto': producto})

@login_required
def subir_imagen_producto(request, pk):
    from django.contrib.auth.decorators import permission_required
    if not (request.user.is_staff or request.user.has_perm('skincare.change_producto')):
        return redirect('inicio')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST' and request.FILES.get('imagen'):
        producto.imagen = request.FILES['imagen']
        producto.save()
        return redirect('detalle_producto', pk=pk)
    return render(request, 'skincare/subir_imagen.html', {'producto': producto})

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    ya_es_favorito = False
    if request.user.is_authenticated:
        from .models import FavoritoProducto
        ya_es_favorito = FavoritoProducto.objects.filter(usuario=request.user, producto=producto).exists()
    return render(request, 'skincare/detalle.html', {
        'producto': producto,
        'ya_es_favorito': ya_es_favorito
    })

@login_required
def toggle_favorito_producto(request, pk):
    from .models import FavoritoProducto
    producto = get_object_or_404(Producto, pk=pk)
    favorito = FavoritoProducto.objects.filter(usuario=request.user, producto=producto)
    if favorito.exists():
        favorito.delete()
        messages.success(request, 'Eliminado de favoritos')
    else:
        FavoritoProducto.objects.create(usuario=request.user, producto=producto)
        messages.success(request, 'Guardado en favoritos')
    return redirect('detalle_producto', pk=pk)
