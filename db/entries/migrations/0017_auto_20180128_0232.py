# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-28 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0016_auto_20180128_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feelingsneedsentry',
            name='public',
            field=models.CharField(choices=[('FALSE', 'false'), ('TRUE', 'true')], default='FALSE', max_length=5),
        ),
    ]