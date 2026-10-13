"""Migración inicial para la aplicación de usuarios."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Crea el modelo Perfil asociado al usuario."""

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('foto', models.ImageField(blank=True, null=True, upload_to='perfiles/')),
                ('bio', models.TextField(blank=True)),
                (
                    'usuario',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
        ),
    ]