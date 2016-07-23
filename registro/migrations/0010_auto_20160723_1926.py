# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0009_auto_20160723_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReglaAutollenado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='formularioasociado',
            name='entrada_destino',
        ),
        migrations.RemoveField(
            model_name='formularioasociado',
            name='entrada_fuente',
        ),
        migrations.AddField(
            model_name='reglaautollenado',
            name='asociacion',
            field=models.ForeignKey(to='registro.FormularioAsociado'),
        ),
        migrations.AddField(
            model_name='reglaautollenado',
            name='entrada_destino',
            field=models.ForeignKey(related_name='entradadestino', blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AddField(
            model_name='reglaautollenado',
            name='entrada_fuente',
            field=models.ForeignKey(related_name='entradafuente', blank=True, to='registro.Entrada', null=True),
        ),
    ]
