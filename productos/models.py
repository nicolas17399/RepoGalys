
from django.db import models

class Producto(models.Model):
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    cantidad_por_caja = models.IntegerField()
    stock_total = models.IntegerField(default=0)
    stock_carrusel = models.IntegerField(default=0)
    promedio_venta = models.IntegerField(default=0)
    tipo_ubicacion = models.CharField(max_length=50, blank=True, null=True)
    unidades_por_batea = models.IntegerField(default=0)
    stock_max_carrusel = models.IntegerField(default=0)

    class Meta:
        unique_together = ('cliente', 'codigo')

    def __str__(self):
        return f"{self.cliente} - {self.codigo}"
