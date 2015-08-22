# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)),
                ('title', models.CharField(unique=True, max_length=120)),
                ('slug', models.SlugField(unique=True, max_length=120)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('published', models.BooleanField(default=False)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('cover_image_url', models.URLField(null=True, verbose_name=b'Cover Image URL', blank=True)),
                ('cover_image_file', models.ImageField(upload_to=b'covers/', null=True, verbose_name=b'Cover Image', blank=True)),
                ('meta_image_url', models.URLField(null=True, verbose_name=b'Meta Image URL', blank=True)),
                ('meta_image_file', models.ImageField(upload_to=b'metas/', null=True, verbose_name=b'Meta Image', blank=True)),
            ],
            options={
                'ordering': ('-date',),
                'get_latest_by': 'date',
            },
        ),
    ]
