from django.db import models
from django.db.models.deletion import PROTECT
from apps.category.models import Category
from apps.sizes.models import Sizes


class Model(models.Model):

    category = models.ForeignKey(
        Category,
        related_name="models",
        on_delete=models.PROTECT,
        verbose_name="Categoria",
    )
    name = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Nombre del modelo",
    )
    sizes = models.ManyToManyField(
        Sizes,
        through="SizesAndModels",
        verbose_name="Tallas",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creacion"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de Actualizacion"
    )

    class Meta:
        db_table = "models"

    def __str__(self):
        return self.name


class SizesAndModels(models.Model):
    size = models.ForeignKey(Sizes, on_delete=PROTECT, verbose_name="Talla")
    model = models.ForeignKey(Model, on_delete=PROTECT, verbose_name="Modelo")
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Précio",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización",
    )

    class Meta:
        db_table = "models_sizes"

    def __str__(self):
        return str(self.id)
