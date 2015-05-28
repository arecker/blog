# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribing', '0002_auto_20150528_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
