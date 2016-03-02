# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0024_auto_20160302_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacionentrada',
            name='regla_visibilidad',
            field=models.ForeignKey(related_name='visibilizar', blank=True, to='registro.ReglaVisibilidad', null=True),
        ),
    ]
