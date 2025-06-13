
from django.urls import path
from . import views
from .views import comparar_cantidades


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('subir_excel/', views.subir_excel, name='subir_excel'),
    path('subir_excel/descargar/', views.descargar_plantilla, name='descargar_plantilla'),
    path('backup/', views.crear_backup, name='crear_backup'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('subir_ubicaciones/', views.subir_ubicaciones, name='subir_ubicaciones'),
    path('analisis_ocupacion/', views.analisis_ocupacion, name='analisis_ocupacion'),
    path('armar_reposicion/', views.armar_reposicion, name='armar_reposicion'),
    path('reposicion_reactiva/', views.reposicion_reactiva, name='reposicion_reactiva'),
    path('descargar_reposicion_reactiva/', views.descargar_reposicion_reactiva, name='descargar_reposicion_reactiva'),
    path('descargar_codigos_faltantes/', views.descargar_codigos_faltantes, name='descargar_codigos_faltantes'),
    path('cargar_productos_generales/', views.cargar_productos_generales, name='cargar_productos_generales'),
    path('comparar_cantidades/', comparar_cantidades, name='comparar_cantidades')
]

