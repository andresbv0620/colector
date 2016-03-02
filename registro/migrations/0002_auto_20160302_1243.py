# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormularioAsociado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seleccionar_existentes', models.BooleanField(default=False)),
                ('crear_nuevo', models.BooleanField(default=False)),
                ('actualizar_existente', models.BooleanField(default=False)),
                ('seleccionar_multiples', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='entrada',
            name='form_asociado',
        ),
        migrations.AddField(
            model_name='formularioasociado',
            name='entrada_destino',
            field=models.ForeignKey(related_name='entradadestino', blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AddField(
            model_name='formularioasociado',
            name='entrada_fuente',
            field=models.ForeignKey(related_name='entradafuente', blank=True, to='registro.Entrada', null=True),
        ),
        migrations.AddField(
            model_name='formularioasociado',
            name='form_asociado',
            field=models.ForeignKey(to='registro.Formulario'),
        ),
        migrations.AddField(
            model_name='asignacionentrada',
            name='formulario_asociado',
            field=models.ForeignKey(related_name='formasociado', blank=True, to='registro.FormularioAsociado', null=True),
        ),
    ]
