# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0013_auto_20150812_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='tablets',
            field=models.ManyToManyField(to='registro.Tablet', blank=True),
        ),
    ]
