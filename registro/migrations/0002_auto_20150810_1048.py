# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='colector',
            field=models.ManyToManyField(to='registro.Colector', blank=True),
        ),
    ]
