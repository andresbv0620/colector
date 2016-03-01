# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0019_auto_20160216_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenEntradaFormulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='entrada',
            name='peso',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='entrada',
            name='precargado',
            field=models.CharField(default=b'NO', max_length=2, choices=[(b'SI', b'SI'), (b'NO', b'NO')]),
        ),
        migrations.AlterField(
            model_name='entrada',
            name='descripcion',
            field=models.TextField(max_length=100, blank=True),
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
            model_name='ordenentradaformulario',
            name='entrada',
            field=models.ForeignKey(blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AddField(
            model_name='ordenentradaformulario',
            name='ficha',
            field=models.ForeignKey(blank=True, to='registro.Ficha', null=True),
        ),
        migrations.AddField(
            model_name='ordenentradaformulario',
            name='formulario',
            field=models.ForeignKey(blank=True, to='registro.Formulario', null=True),
        ),
    ]
