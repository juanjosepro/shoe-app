from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre de la categoría')
    description = models.TextField(max_length=250, blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name
