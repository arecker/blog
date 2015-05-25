# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_created=True)),
                ('email', models.EmailField(max_length=254)),
                ('full_text', models.BooleanField(default=False)),
                ('key', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
    ]
