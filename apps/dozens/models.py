from apps.sizes.models import Sizes
from django.db import models
from django.db.models.deletion import PROTECT
from apps.model.models import Model
from apps.sizes.models import Sizes

class Dozen(models.Model):


    material_choices = (
        ('cuero', 'cuero'),
        ('gamusa', 'gamusa'),
    )

    status_choices = (
        ('disponible', 'disponible'),
        ('vendido', 'vendido'),
    )


    model = models.ForeignKey(Model, related_name='models', on_delete=PROTECT, blank=False, verbose_name='Modelo')
    sizes = models.ForeignKey(Sizes, related_name='sizes', on_delete=PROTECT, blank=False, verbose_name='Talla')
    amount = models.IntegerField(blank=False, verbose_name='Cantidad')
    color = models.CharField(max_length=30, blank=False, verbose_name='Color')
    material = models.CharField(max_length=30, blank=False, choices=material_choices, default='cuero', verbose_name='Material')
    status = models.CharField(max_length=30, blank=False, choices=status_choices, default='disponible', verbose_name='Estado')
    note = models.TextField(max_length=30, null=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')
    class Meta:
        db_table = 'dozens'
    
    def __str__(self):
        return str(self.created_at)