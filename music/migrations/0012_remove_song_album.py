# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 16:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_song_album'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='album',
        ),
    ]
