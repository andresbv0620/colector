# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0018_empresa_codigo_secreto'),
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
                ('maximo', models.PositiveIntegerField()),
                ('minimo', models.PositiveIntegerField()),
                ('validacion', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ('orden',),
            },
        ),
        migrations.CreateModel(
            name='ReglaVisibilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operador', models.CharField(max_length=50, choices=[(b'igual_a', b'Igual a'), (b'no_igual_a', b'No igual a'), (b'contiene', b'Contiene'), (b'empieza_con', b'Empieza con'), (b'mayor_que', b'Mayor que'), (b'menor_que', b'Menor que'), (b'es_vacio', b'Es vacio'), (b'no_es_vacio', b'No es vacio')])),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='ficha',
            name='entrada',
        ),
        migrations.AddField(
            model_name='entrada',
            name='form_asociado',
            field=models.ForeignKey(blank=True, to='registro.Formulario', null=True),
        ),
        migrations.AddField(
            model_name='formulario',
            name='precargado',
            field=models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='descripcion',
            field=models.TextField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'SCAN'), (b'10', b'DINAMICA UNICA'), (b'11', b'DINAMICA MULTIPLE'), (b'12', b'GPS'), (b'13', b'FORMULA'), (b'14', b'FIRMA'), (b'15', b'DECIMAL')]),
        ),
        migrations.AlterField(
            model_name='ficha',
            name='descripcion',
            field=models.TextField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='descripcion',
            field=models.TextField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='valor',
            field=models.CharField(unique=True, max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='reglavisibilidad',
            name='elemento',
            field=models.OneToOneField(to='registro.Entrada'),
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
            field=models.OneToOneField(null=True, blank=True, to='registro.ReglaVisibilidad'),
        ),
        migrations.AddField(
            model_name='ficha',
            name='entrada2',
            field=models.ManyToManyField(to='registro.Entrada', through='registro.AsignacionEntrada', blank=True),
        ),
    ]
