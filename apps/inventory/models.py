from django.db import models
from apps.materials.models import Material
from apps.providers_and_customers.models import ProvidersAndCustomers


class Inventory(models.Model):
    colors_choices = (
        ('negro', 'negro'),
        ('plomo', 'plomo'),
        ('cafe', 'cafe'),
        ('amarillo', 'amarillo'),
        ('verde', 'verde'),
        ('blanco', 'rojo'),
        ('azul', 'azul'),
        ('rojo', 'rojo'),
    )

    material = models.ForeignKey(Material, related_name='inventory', on_delete=models.PROTECT, verbose_name='Material')
    provider = models.ForeignKey(ProvidersAndCustomers, null=True, blank=True, related_name='inventory', on_delete=models.PROTECT, verbose_name='Proveedor')
    amount = models.IntegerField(verbose_name='Cantidad')
    stock = models.IntegerField(verbose_name='Existencias')
    color = models.CharField(max_length=15, choices=colors_choices, blank=True, verbose_name='Color')
    type = models.CharField(max_length=250, blank=True, verbose_name='Tipo de material') # string cuero,gamusa,sintetico,etc
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Precio')
    note = models.TextField(max_length=255, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'inventory'

    def __str__(self):
        return self.type
