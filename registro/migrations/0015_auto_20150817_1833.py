# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0014_auto_20150817_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermisoFormulario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colectores', models.ManyToManyField(to='registro.Colector')),
                ('formulario', models.ForeignKey(to='registro.Formulario')),
            ],
        ),
        migrations.AlterField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'TEXTO'), (b'2', b'PARRAFO'), (b'3', b'OPCION'), (b'4', b'UNICA'), (b'5', b'MULTIPLE'), (b'6', b'FOTO'), (b'7', b'FECHA'), (b'8', b'NUMERO'), (b'9', b'FOTO'), (b'10', b'FECHA'), (b'11', b'NUMERO')]),
        ),
    ]
