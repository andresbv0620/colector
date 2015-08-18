# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0005_auto_20150810_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formulario_diligenciado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='entrada',
            name='respuesta',
            field=models.ManyToManyField(to='registro.Respuesta', blank=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='Formulario_diligenciado',
            field=models.ManyToManyField(to='registro.Formulario_diligenciado', blank=True),
        ),
        migrations.AddField(
            model_name='ficha',
            name='entrada',
            field=models.ManyToManyField(to='registro.Entrada', blank=True),
        ),
    ]
