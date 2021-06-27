from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre')
    types = models.CharField(max_length=250, blank=True, verbose_name='Tipos')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'materials'

    def __str__(self):
        return self.name
