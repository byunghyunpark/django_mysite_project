# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0004_auto_20161027_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='img_thumbnail',
            field=models.ImageField(blank=True, upload_to='photo/thumbnail'),
        ),
    ]