from django.db import models

# Create your models here.
class Sizes(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre')
    size = models.CharField(max_length=30, verbose_name='Talla')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')
    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name