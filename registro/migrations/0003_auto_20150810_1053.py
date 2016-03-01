# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0002_auto_20150810_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='plan',
            field=models.ForeignKey(blank=True, to='registro.Plan', null=True),
        ),
    ]
