# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-05 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_song_audio_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='album',
        ),
    ]
