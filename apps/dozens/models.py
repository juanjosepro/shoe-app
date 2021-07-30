from apps.sizes.models import Sizes
from django.db import models
from django.db.models.deletion import PROTECT
from django.contrib.auth.models import User
from django.conf import settings
from apps.model.models import Model
from apps.sizes.models import Sizes


class Dozen(models.Model):
    material_choices = (
        ("cuero", "cuero"),
        ("gamusa", "gamusa"),
        ("sin_especificar", "sin especificar"),
    )
    statuses_choices = (
        ("disponible", "disponible (1)"),
        ("aparado_en_produccion", "Aparado en producción (2)"),
        ("aparado_finalizado", "Aparado finalizado (3)"),
        ("armado_en_produccion", "Armado en producción (4)"),
        ("armado_finalizado", "Armado finalizado (5)"),
        ("produccion_finalizada", "Produccion finalizada (6)"),
        ("vendido", "Docena Vendida"),
    )
    colors_choices = (
        ("negro", "negro"),
        ("plomo", "plomo"),
        ("cafe", "cafe"),
        ("amarillo", "amarillo"),
        ("verde", "verde"),
        ("blanco", "rojo"),
        ("azul", "azul"),
        ("rojo", "rojo"),
        ("sin_especificar", "sin especificar"),
    )

    model = models.ForeignKey(
        Model, related_name="dozens", on_delete=PROTECT, verbose_name="Modelo"
    )
    size = models.ForeignKey(
        Sizes, related_name="dozens", on_delete=PROTECT, verbose_name="Talla"
    )
    material = models.CharField(
        max_length=30,
        choices=material_choices,
        default="cuero",
        verbose_name="Elija el Material",
    )
    color = models.CharField(
        max_length=30, choices=colors_choices, verbose_name="Elija el Color"
    )
    status = models.CharField(
        max_length=30,
        choices=statuses_choices,
        default="disponible",
        verbose_name="Estado actual de la docena",
    )
    note = models.TextField(max_length=250, blank=True, verbose_name="¿Desea agregar alguna nota sobre esta docena?")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        db_table = "dozens"

    def __str__(self):
        return str(self.id)


class DozensOfCortadores(models.Model):
    dozen = models.OneToOneField(
        Dozen, related_name="cortador", on_delete=PROTECT, verbose_name="Docena"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="cortadores",
        on_delete=PROTECT,
        verbose_name="Cortadores",
    )
    note = models.TextField(max_length=250, blank=True, verbose_name="Nota")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        db_table = "dozens_of_cortadores"

    def __str__(self):
        return str(self.id)


class DozensOfAparadores(models.Model):
    statuses_choices = (
        ("produccion", "aparado en producción"),
        ("finalizado", "aparado finalizado"),
    )

    dozen = models.OneToOneField(
        Dozen, related_name="aparador", on_delete=PROTECT, verbose_name="Docena"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="aparadores",
        on_delete=PROTECT,
        verbose_name="Aparadores",
    )
    status = models.CharField(
        max_length=30, choices=statuses_choices, verbose_name="Estado"
    )
    note = models.TextField(max_length=250, blank=True, verbose_name="Nota")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        db_table = "dozens_of_aparadores"

    def __str__(self):
        return str(self.id)


class DozensOfArmadores(models.Model):
    statuses_choices = (
        ("produccion", "armado en produccion"),
        ("finalizado", "armado finalizado"),
    )

    dozen = models.OneToOneField(
        Dozen, related_name="armador", on_delete=PROTECT, verbose_name="Docena"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="armadores",
        on_delete=PROTECT,
        verbose_name="Armadores",
    )
    status = models.CharField(
        max_length=30, choices=statuses_choices, verbose_name="Estado"
    )
    note = models.TextField(max_length=250, blank=True, verbose_name="Nota")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        db_table = "dozens_of_armadores"

    def __str__(self):
        return str(self.id)


class DozensOfRematadores(models.Model):
    dozen = models.OneToOneField(
        Dozen, related_name="rematador", on_delete=PROTECT, verbose_name="Docena"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="rematadores",
        on_delete=PROTECT,
        verbose_name="Rematadores",
    )
    note = models.TextField(max_length=250, blank=True, verbose_name="Nota")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        db_table = "dozens_of_rematadores"

    def __str__(self):
        return str(self.id)
