from django.db import models
from django.contrib.auth.models import User

class Nota(models.Model):
    usuario   = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo    = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)
    editado   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} — {self.titulo}"