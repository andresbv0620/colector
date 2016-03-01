# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0010_auto_20150812_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='tipo',
            field=models.CharField(default=b'FR', max_length=2, choices=[(b'FR', b'Freshman'), (b'SO', b'Sophomore'), (b'JR', b'Junior'), (b'SR', b'Senior')]),
        ),
    ]
