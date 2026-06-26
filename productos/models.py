from django.db import models
from django.utils import timezone


class ProductoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(eliminado=False)


class Producto(models.Model):
    id_productos = models.AutoField(primary_key=True, db_column='id_productos')
    nombre = models.CharField(max_length=45)
    cantidad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(null=True, blank=True)
    stock_minimo = models.IntegerField(default=5)
    estado = models.CharField(max_length=20, default='pendiente')
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    eliminado_por_id = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = ProductoManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'tblproducto'

    def soft_delete(self, user_id=None):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.eliminado_por_id = user_id
        self.save()

    def __str__(self):
        return self.nombre
