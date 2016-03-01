# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0019_auto_20160218_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ficha',
            old_name='entrada2',
            new_name='entrada',
        ),
    ]
