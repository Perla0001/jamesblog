from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('hidratante', 'Hidratante'),
        ('protector',  'Protector Solar'),
        ('serum',      'Sérum'),
        ('limpiador',  'Limpiador'),
        ('otro',       'Otro'),
    ]
    nombre      = models.CharField(max_length=200)
    marca       = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria   = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    imagen      = models.ImageField(upload_to='skincare/', blank=True, null=True)
    guia_latam  = models.TextField(blank=True)
    guia_europa = models.TextField(blank=True)

    def __str__(self):
        return f"{self.marca} — {self.nombre}"

class FavoritoProducto(models.Model):
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'producto')