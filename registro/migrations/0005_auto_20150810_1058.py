# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0004_auto_20150810_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='formulario',
            name='ficha',
            field=models.ManyToManyField(to='registro.Ficha', blank=True),
        ),
    ]
