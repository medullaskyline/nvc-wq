# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-08 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_auto_20180108_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeling',
            name='main_category',
            field=models.CharField(choices=[('EMOTIONAL', 'emotional'), ('MENTAL', 'mental'), ('PHYSICAL', 'physical')], editable=False, max_length=256),
        ),
        migrations.AlterField(
            model_name='feeling',
            name='sub_category',
            field=models.CharField(choices=[('ANGER', 'anger'), ('DISGUST', 'disgust'), ('ENJOYMENT', 'enjoyment'), ('FEAR', 'fear'), ('SADNESS', 'sadness'), ('AVERSION', 'aversion'), ('CONFUSION', 'confusion'), ('CONNECTED', 'connected'), ('DISCONNECTED', 'disconnected'), ('GRASPING', 'grasping'), ('SURPRISE', 'surprise'), ('ENERGY', 'energy'), ('FOOD/DRINK', 'food/drink'), ('PAIN/PLEASURE', 'pain/pleasure'), ('TEMPERATURE', 'temperature')], editable=False, max_length=256),
        ),
    ]
