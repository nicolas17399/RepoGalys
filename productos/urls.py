
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('subir_excel/', views.subir_excel, name='subir_excel'),
    path('subir_excel/descargar/', views.descargar_plantilla, name='descargar_plantilla'),
    path('crear_backup/', views.crear_backup, name='crear_backup'),
]
