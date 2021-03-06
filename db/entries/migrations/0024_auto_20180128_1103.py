# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-28 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0023_auto_20180128_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feelingmaincategory',
            options={'verbose_name_plural': 'Feeling Categories'},
        ),
        migrations.AlterModelOptions(
            name='feelingsubcategory',
            options={'verbose_name_plural': 'Feeling Subcategories'},
        ),
        migrations.AlterModelOptions(
            name='needcategory',
            options={'verbose_name_plural': 'Need Categories'},
        ),
        migrations.AddField(
            model_name='feelingleaf',
            name='main_category',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='entries.FeelingMainCategory'),
            preserve_default=False,
        ),
    ]
