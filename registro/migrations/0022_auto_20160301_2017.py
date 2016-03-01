# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0021_auto_20160301_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reglavisibilidad',
            name='elemento',
            field=models.ForeignKey(to='registro.Entrada'),
        ),
    ]
