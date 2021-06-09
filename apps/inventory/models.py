from django.db import models
from apps.materials.models import Material


class Inventory(models.Model):
    material = models.ForeignKey(Material, related_name='material', on_delete=models.PROTECT, blank=False, verbose_name='Inventario')
    amount = models.IntegerField(blank=False, verbose_name='Cantidad')
    color = models.CharField(max_length=250, null=True, blank=False, verbose_name='Color')
    type = models.CharField(max_length=250, null=False, blank=False, verbose_name='Tipo de material')
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, verbose_name='Tipo de material')
    note = models.TextField(max_length=255, null=True, blank=False, verbose_name='Nota')
    created_at = models.DateField(auto_now=True, verbose_name='Fecha de creacion')

    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return self.type