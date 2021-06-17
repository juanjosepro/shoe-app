from django.db import models
from apps.materials.models import Material


class Inventory(models.Model):
    material = models.ForeignKey(Material, related_name='material', on_delete=models.PROTECT, verbose_name='Inventario')
    amount = models.IntegerField(verbose_name='Cantidad')
    color = models.CharField(max_length=250, blank=True, verbose_name='Color')
    type = models.CharField(max_length=250, blank=True, verbose_name='Tipo de material')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tipo de material')
    note = models.TextField(max_length=255, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return self.type
