# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 00:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160627_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitterdata',
            name='followers_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='friends_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='refreshed_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 27, 0, 24, 33, 432461)),
        ),
        migrations.AlterField(
            model_name='twitterdata',
            name='screen_name',
            field=models.TextField(default=''),
        ),
    ]
