# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0003_auto_20150810_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='formulario',
            field=models.ManyToManyField(to='registro.Formulario', blank=True),
        ),
    ]
