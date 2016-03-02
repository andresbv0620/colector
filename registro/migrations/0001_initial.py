# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionEntrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.PositiveIntegerField()),
                ('requerido', models.BooleanField(default=False)),
                ('oculto', models.BooleanField(default=False)),
                ('solo_lectura', models.BooleanField(default=False)),
                ('defecto', models.CharField(max_length=50, blank=True)),
                ('defecto_previo', models.BooleanField(default=False)),
                ('maximo', models.PositiveIntegerField(null=True, blank=True)),
                ('minimo', models.PositiveIntegerField(null=True, blank=True)),
                ('validacion', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ('orden',),
            },
        ),
        migrations.CreateModel(
            name='Colector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_secreto', models.CharField(max_length=50)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('industria', models.CharField(max_length=50, blank=True)),
                ('pais', models.CharField(max_length=50, blank=True)),
                ('ciudad', models.CharField(max_length=50, blank=True)),
                ('correo_empresarial', models.TextField(max_length=50, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('descripcion', models.TextField(max_length=50, blank=True)),
                ('nit', models.IntegerField(null=True, blank=True)),
                ('correo_facturacion', models.CharField(unique=True, max_length=50, blank=True)),
                ('telefono', models.IntegerField(null=True, blank=True)),
                ('colector', models.ManyToManyField(to='registro.Colector', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'SCAN'), (b'10', b'DINAMICA UNICA'), (b'11', b'DINAMICA MULTIPLE'), (b'12', b'GPS'), (b'13', b'FORMULA'), (b'14', b'FIRMA'), (b'15', b'DECIMAL')])),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('descripcion', models.TextField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('descripcion', models.TextField(max_length=100, blank=True)),
                ('entrada', models.ManyToManyField(to='registro.Entrada', through='registro.AsignacionEntrada', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('descripcion', models.TextField(max_length=100, blank=True)),
                ('precargado', models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')])),
                ('ficha', models.ManyToManyField(to='registro.Ficha', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormularioDiligenciado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('gps', models.CharField(unique=True, max_length=50, blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('colector', models.ForeignKey(blank=True, to='registro.Colector', null=True)),
                ('empresa', models.ForeignKey(blank=True, to='registro.Empresa', null=True)),
                ('entrada', models.ForeignKey(blank=True, to='registro.Entrada', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PermisoFormulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colectores', models.ManyToManyField(to='registro.Colector')),
                ('formulario', models.ForeignKey(to='registro.Formulario')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('almacenamiento', models.CharField(unique=True, max_length=50, blank=True)),
                ('cantidad_colectores', models.IntegerField(unique=True, blank=True)),
                ('valor', models.CharField(unique=True, max_length=50, blank=True)),
                ('activo', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReglaVisibilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operador', models.CharField(max_length=50, choices=[(b'igual_a', b'Igual a'), (b'no_igual_a', b'No igual a'), (b'contiene', b'Contiene'), (b'empieza_con', b'Empieza con'), (b'mayor_que', b'Mayor que'), (b'menor_que', b'Menor que'), (b'es_vacio', b'Es vacio'), (b'no_es_vacio', b'No es vacio')])),
                ('valor', models.CharField(max_length=100)),
                ('elemento', models.ForeignKey(to='registro.Entrada')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(unique=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='formulariodiligenciado',
            name='respuesta',
            field=models.ForeignKey(blank=True, to='registro.Respuesta', null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='form_asociado',
            field=models.ForeignKey(blank=True, to='registro.Formulario', null=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='respuesta',
            field=models.ManyToManyField(to='registro.Respuesta', blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='formulario',
            field=models.ManyToManyField(to='registro.Formulario', blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='plan',
            field=models.ForeignKey(blank=True, to='registro.Plan', null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='tablets',
            field=models.ManyToManyField(to='registro.Tablet', blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asignacionentrada',
            name='entrada',
            field=models.ForeignKey(to='registro.Entrada'),
        ),
        migrations.AddField(
            model_name='asignacionentrada',
            name='ficha',
            field=models.ForeignKey(to='registro.Ficha'),
        ),
        migrations.AddField(
            model_name='asignacionentrada',
            name='regla_visibilidad',
            field=models.ForeignKey(related_name='visibilizar', blank=True, to='registro.ReglaVisibilidad', null=True),
        ),
    ]
