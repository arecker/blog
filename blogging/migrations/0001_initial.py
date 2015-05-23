# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=120)),
                ('slug', models.SlugField(unique=True, max_length=120)),
                ('date', models.DateField(default=datetime.datetime(2015, 5, 23, 18, 51, 22, 909249))),
                ('published', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('image_url', models.URLField(null=True, verbose_name=b'Image URL', blank=True)),
            ],
        ),
    ]
