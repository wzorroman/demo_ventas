from django.db import models


class Producto(models.Model):
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.descripcion}'
