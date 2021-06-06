from django.db import models
from apps.product.models import Product

# Create your models here.
class Sizes(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.PROTECT, blank=False, verbose_name='Producto')
    name = models.CharField(max_length=30, unique=True,  blank=False, verbose_name='Nombre')
    note = models.TextField(max_length=255, null=True, verbose_name='Nota')
    created_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name