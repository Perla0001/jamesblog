"""Modelos para la aplicación de usuarios."""

from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """Modelo que extiende el usuario con foto y biografía."""

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto    = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    bio     = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"