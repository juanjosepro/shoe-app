from django.db import models
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name='Nombre')
    created_at = models.DateField(auto_now=True)


    class Meta:
        db_table = 'products'
        
    def __str__(self):
        return self.name
