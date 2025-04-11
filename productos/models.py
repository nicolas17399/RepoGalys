from django.db import models

class Producto(models.Model):
    cliente_codigo = models.CharField(max_length=100)
    stock_total = models.IntegerField(default=0)
    stock_carrusel = models.IntegerField(default=0)
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    cantidad_por_caja = models.IntegerField(default=1)
    promedio_venta = models.IntegerField(default=0)
    promedio_sobredimensionado=models.IntegerField(default=0)
    cantidad_op=models.IntegerField(default=0)
    tipo_ubicacion = models.CharField(max_length=50, blank=True, null=True)
    unidades_por_batea = models.IntegerField(default=0)
    cantidad_bateas=models.IntegerField(default=0)
    cantidad_max_bateas=models.IntegerField(default=0)
    stock_max_carrusel = models.IntegerField(default=0)
    psicofarmaco = models.CharField(max_length=100, default='No informado')

    def __str__(self):
        return self.cliente_codigo
