# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 09:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0009_auto_20170510_0710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='geniuspost',
            old_name='last_comment_datetime',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='redditpost',
            old_name='post_datetime',
            new_name='datetime',
        ),
    ]