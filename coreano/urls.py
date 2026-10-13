from django.urls import path
from . import views

urlpatterns = [
    path('', views.estudio_view, name='estudio'),
    path('notas/', views.lista_notas, name='lista_notas'),
    path('notas/crear/', views.crear_nota, name='crear_nota'),
    path('notas/<int:pk>/eliminar/', views.eliminar_nota, name='eliminar_nota'),
]