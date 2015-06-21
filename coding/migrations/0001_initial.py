# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'projects', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'URL', blank=True)),
            ],
        ),
    ]
