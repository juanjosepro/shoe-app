from django.db import models
from django.db.models.deletion import PROTECT
from apps.providers_and_customers.models import ProvidersAndCustomers

# Create your models here.
class Sales(models.Model):
    statuses = (
        ('al contado', 'al contado'),
        ('giro', 'giro'),
        ('deposito', 'deposito'),
    )

    customer = models.ForeignKey(ProvidersAndCustomers, on_delete=PROTECT, verbose_name='Clientes')
    dozens_list = models.CharField(max_length=250, verbose_name='Lista de docenas por id')
    number_of_dozens = models.IntegerField(verbose_name='Cantidad')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Total precio')
    money_paid = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Dinero pagado')
    total_money_owed = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Dinero total adeudado')
    status = models.CharField(choices=statuses,default='al contado', max_length=30, verbose_name='Estado')
    note = models.TextField(max_length=250, blank=True, verbose_name='Nota')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')

    class Meta:
        db_table = 'sales'

    def __str__(self):
        return str(self.created_at)