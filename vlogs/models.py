from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    DESTINO_CHOICES = [
        ('corea', 'Corea del Sur'),
        ('tailandia', 'Tailandia'),
    ]
    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField()
    destino     = models.CharField(max_length=20, choices=DESTINO_CHOICES)
    imagen      = models.ImageField(upload_to='vlogs/', blank=True, null=True)
    fecha       = models.DateTimeField(auto_now_add=True)
    autor       = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'post')

class Comentario(models.Model):
    post      = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=500)
    fecha     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} en {self.post.titulo}"