# Generated by Django 3.2.3 on 2021-06-12 13:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('sizes', '0001_initial'),
        ('model', '0004_auto_20210612_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='category',
            field=models.ForeignKey(default=None, help_text='Seleccione la categoria a la que pertenecerá este modelo', on_delete=django.db.models.deletion.PROTECT, related_name='models', to='category.category', verbose_name='Categoria'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='model',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de Creacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='model',
            name='name',
            field=models.CharField(default=None, help_text='Nombre del modelo', max_length=30, unique=True, verbose_name='Nombre'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='model',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Precio de este modelo', max_digits=5, verbose_name='Precio'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='model',
            name='sizes',
            field=models.ManyToManyField(help_text='¿Que tallas va  a tener este modelo?', through='model.SizesAndModels', to='sizes.Sizes', verbose_name='Tallas'),
        ),
        migrations.AddField(
            model_name='model',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion'),
        ),
        migrations.AlterModelTable(
            name='model',
            table='models',
        ),
    ]