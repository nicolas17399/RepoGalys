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

class UbicacionCarrusel(models.Model):
    id_posicion = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    entrando = models.IntegerField(default=0)
    saliendo = models.IntegerField(default=0)
    denominacion = models.CharField(max_length=255, blank=True)
    lote = models.CharField(max_length=100, blank=True)
    caducidad = models.CharField(max_length=100, blank=True)
    udc = models.CharField(max_length=100, blank=True)
    uds_udc = models.IntegerField(default=0)
    ultima_entrada = models.CharField(max_length=100, blank=True)
    anchura = models.FloatField(default=0)
    profundidad = models.FloatField(default=0)
    altura = models.FloatField(default=0)
    zona = models.CharField(max_length=50, blank=True)
    equipo = models.CharField(max_length=50, blank=True)
    modulo = models.CharField(max_length=50, blank=True)
    nivel = models.CharField(max_length=50, blank=True)
    fondo = models.CharField(max_length=50, blank=True)
    articulo = models.CharField(max_length=100, blank=True)
    reservado_articulo = models.CharField(max_length=50, blank=True)
    reservado_udc = models.CharField(max_length=50, blank=True)
    fija = models.CharField(max_length=50, blank=True)
    cod_barras = models.CharField(max_length=100, blank=True)
    udc_reserva = models.CharField(max_length=100, blank=True)
    bloqueada = models.CharField(max_length=50, blank=True)
    impedir_entrada = models.CharField(max_length=50, blank=True)
    impedir_salida = models.CharField(max_length=50, blank=True)
    udp = models.CharField(max_length=50, blank=True)
    uds_udp = models.IntegerField(default=0)
    tipo_stock = models.CharField(max_length=50, blank=True)
    propietario = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.ubicacion} ({self.stock})"

    @property
    def porcentaje_ocupacion(self):
        try:
            if self.stock == 0 or str(self.ubicacion).lower().endswith('i'):
                return 0
            return round((self.stock / self.uds_udc) * 100, 2)
        except:
            return 0

    @property
    def clasificacion_ocupacion(self):
        if str(self.ubicacion).lower().endswith('i'):
            return 'Ficticia'

        porcentaje = self.porcentaje_ocupacion
        if porcentaje == 0:
            return 'Vacía'
        elif 0 < porcentaje <= 10:
            return 1
        elif 10 < porcentaje <= 20:
            return 2
        elif 20 < porcentaje <= 30:
            return 3
        elif 30 < porcentaje <= 40:
            return 4
        elif 40 < porcentaje <= 50:
            return 5
        elif 50 < porcentaje <= 60:
            return 6
        elif 60 < porcentaje <= 70:
            return 7
        elif 70 < porcentaje <= 80:
            return 8
        elif 80 < porcentaje <= 90:
            return 9
        else:
            return 10
        
class PedidoTemporal(models.Model):
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    lote = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.cliente} - {self.codigo} - {self.cantidad}"

class ProductoGeneral(models.Model):
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    galys = models.BooleanField(default=False)
    cantidad_por_caja = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('cliente', 'codigo')

    def __str__(self):
        return f"{self.cliente} - {self.codigo}"