# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-12 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0017_album_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
