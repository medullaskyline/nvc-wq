# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-18 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0012_auto_20180115_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feelingsneedsentry',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
