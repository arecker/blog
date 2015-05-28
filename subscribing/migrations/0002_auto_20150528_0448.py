# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('subscribing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='id',
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True),
        ),
    ]
