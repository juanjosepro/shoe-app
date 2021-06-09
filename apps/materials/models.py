from django.db import models

# Create your models here.
class Material(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, blank=False, verbose_name='Nombre')
    types = models.CharField(max_length=250, null=False, blank=False, verbose_name='Tipos')

    class Meta:
        db_table = 'materials'

    def __str__(self):
        return self.name
