
from django.urls import path
from . import views

urlpatterns = [
    path('subir_excel/', views.subir_excel, name='subir_excel'),
    path('subir_stock/', views.subir_stock, name='subir_stock'),
    path('subir_reposicion/', views.subir_reposicion, name='subir_reposicion'),
]
