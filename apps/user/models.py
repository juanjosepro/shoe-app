from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name='Telefono')
    direction = models.TextField(max_length=255, blank=True, verbose_name='Dirección')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')

    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "Usuarios"