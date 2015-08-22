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
                ('key', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('verified', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
