# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0003_auto_20160323_0521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrada',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'ordering': ('id',)},
        ),
    ]
