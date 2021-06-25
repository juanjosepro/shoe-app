from django.db import models
from django.db.models.deletion import PROTECT
from django.contrib.auth.models import User
from apps.dozens.models import Dozen


""" class DozensOfCortadores(models.Model):
    
    dozen = models.OneToOneField(Dozen, related_name='cortador', on_delete=PROTECT, verbose_name='Docena')
    user = models.ForeignKey(User, related_name='cortadores', on_delete=PROTECT, verbose_name='Cortadores')
    note = models.TextField(max_length=250, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'dozens_of_cortadores'

    def __str__(self):
        return str(self.id)


class DozensOfAparadores(models.Model):
    
    statuses_choices = (
        ('produccion', 'aparado en producción'),
        ('finalizado', 'aparado finalizado'),
    )

    dozen = models.OneToOneField(Dozen, related_name='aparador', on_delete=PROTECT, verbose_name='Docena')
    user = models.ForeignKey(User, related_name='aparadores', on_delete=PROTECT, verbose_name='Aparadores')
    status = models.CharField(max_length=30, choices=statuses_choices, verbose_name='Estado')
    note = models.TextField(max_length=250, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'dozens_of_aparadores'

    def __str__(self):
        return str(self.id)


class DozensOfArmadores(models.Model):
    
    statuses_choices = (
        ('produccion', 'armado en produccion'),
        ('finalizado', 'armado finalizado')
    )

    dozen = models.OneToOneField(Dozen, related_name='armador', on_delete=PROTECT, verbose_name='Docena')
    user = models.ForeignKey(User, related_name='armadores', on_delete=PROTECT, verbose_name='Armadores')
    status = models.CharField(max_length=30, choices=statuses_choices, verbose_name='Estado')
    note = models.TextField(max_length=250, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'dozens_of_armadores'

    def __str__(self):
        return str(self.id)


class DozensOfRematadoras(models.Model):
    
    dozen = models.OneToOneField(Dozen, related_name='rematador', on_delete=PROTECT, verbose_name='Docena')
    user = models.ForeignKey(User, related_name='rematadoras', on_delete=PROTECT, verbose_name='Rematadoras')
    note = models.TextField(max_length=250, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'dozens_of_rematadoras'

    def __str__(self):
        return str(self.id) """