# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 06:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualizations', '0006_auto_20170510_0642'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='albumchartrank',
            unique_together=set([('album', 'week')]),
        ),
        migrations.AlterUniqueTogether(
            name='songchartrank',
            unique_together=set([('song_name', 'week')]),
        ),
    ]
