from django.db import models
from apps.category.models import Category

class Model(models.Model):
    
    category = models.ForeignKey(
        Category, related_name='models',
        on_delete=models.PROTECT,
        blank=False,
        verbose_name='Categoria',
        help_text='Seleccione la categoria a la que pertenecerá este modelo',
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        verbose_name='Nombre',
        help_text='Nombre del modelo',
    )
    sizes = models.CharField(
        max_length=120,
        blank=False,
        verbose_name='Tallas',
        help_text='¿Que tallas va  a tener este modelo?',
    )
    price = models.DecimalField(
        max_digits=5,
        blank=False,
        decimal_places=2,
        verbose_name='Precio',
        help_text='Precio de este modelo',
    )

    class Meta:
        db_table = 'models'

    def __str__(self):
        return self.name