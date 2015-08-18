# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0015_auto_20150817_1833'),
    ]

    operations = [
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
                ('respuesta', models.ForeignKey(blank=True, to='registro.Respuesta', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='formulario_diligenciado',
            name='colector',
        ),
        migrations.RemoveField(
            model_name='formulario_diligenciado',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='formulario_diligenciado',
            name='entrada',
        ),
        migrations.RemoveField(
            model_name='formulario_diligenciado',
            name='respuesta',
        ),
        migrations.DeleteModel(
            name='Formulario_diligenciado',
        ),
    ]
