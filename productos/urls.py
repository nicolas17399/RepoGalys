
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('subir_excel/', views.subir_excel, name='subir_excel'),
    path('subir_excel/descargar/', views.descargar_plantilla, name='descargar_plantilla'),
    path('crear_backup/', views.crear_backup, name='crear_backup'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('subir_ubicaciones/', views.subir_ubicaciones, name='subir_ubicaciones'),
    path('analisis_ocupacion/', views.analisis_ocupacion, name='analisis_ocupacion'),
    path('armar_reposicion/', views.armar_reposicion, name='armar_reposicion'),
]

