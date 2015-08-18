# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_token_middleware', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='empresa',
            field=models.OneToOneField(to='registro.Empresa'),
        ),
        migrations.AlterField(
            model_name='token',
            name='valor',
            field=models.CharField(unique=True, max_length=50, blank=True),
        ),
    ]
