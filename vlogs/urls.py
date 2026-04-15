from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('vlogs/', views.lista_vlogs, name='lista_vlogs'),
    path('vlogs/crear/', views.crear_vlog, name='crear_vlog'),
    path('vlogs/<int:pk>/', views.detalle_vlog, name='detalle_vlog'),
    path('vlogs/<int:pk>/editar/', views.editar_vlog, name='editar_vlog'),
    path('vlogs/<int:pk>/eliminar/', views.eliminar_vlog, name='eliminar_vlog'),
    path('vlogs/<int:pk>/favorito/', views.toggle_favorito_vlog, name='toggle_favorito_vlog'),
]