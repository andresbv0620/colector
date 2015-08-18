# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0012_auto_20150812_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='direccion',
            new_name='correo_empresarial',
        ),
        migrations.RenameField(
            model_name='empresa',
            old_name='correo',
            new_name='correo_facturacion',
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Simple'), (b'2', b'Compuesto')]),
        ),
    ]
