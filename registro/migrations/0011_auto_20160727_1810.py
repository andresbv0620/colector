# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0010_auto_20160723_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formulario',
            name='precargado',
        ),
        migrations.AddField(
            model_name='formulario',
            name='titulo_reporte2',
            field=models.ForeignKey(related_name='tituloreporte2', blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='titulo_reporte',
            field=models.ForeignKey(blank=True, to='registro.Entrada', null=True),
        ),
    ]
