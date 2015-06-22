# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0002_auto_20150621_2232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-added']},
        ),
        migrations.AddField(
            model_name='project',
            name='added',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
