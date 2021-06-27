from django.db import models


class Sizes(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre de la talla')
    size = models.CharField(max_length=30, verbose_name='Talla ejemplo 38-42')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name