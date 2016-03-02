# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0023_auto_20160302_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionentrada',
            name='regla_visibilidad',
            field=models.OneToOneField(related_name='visibilizar', null=True, blank=True, to='registro.ReglaVisibilidad'),
        ),
    ]
