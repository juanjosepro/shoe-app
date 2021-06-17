from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre')
    description = models.TextField(max_length=255, blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name
