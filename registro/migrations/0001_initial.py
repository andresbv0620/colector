# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
                ('nit', models.IntegerField(null=True, blank=True)),
                ('correo', models.CharField(unique=True, max_length=50, blank=True)),
                ('telefono', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
