from django.db import models
from apps.product.models import Product


class Category(models.Model):
    product = models.ForeignKey(Product, related_name='categories', on_delete=models.PROTECT, blank=False, verbose_name='Producto')
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name='Nombre')
    description = models.TextField(max_length=255, null=True, verbose_name='Descripción')
    created_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name
