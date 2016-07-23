# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0008_auto_20160713_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario',
            name='titulo_reporte',
            field=models.ForeignKey(default=0, blank=True, to='registro.Entrada', null=True),
        ),
    ]
