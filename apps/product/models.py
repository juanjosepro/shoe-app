from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')

    class Meta:
        db_table = 'products'
        
    def __str__(self):
        return self.name
