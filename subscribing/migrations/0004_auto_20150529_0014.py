# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribing', '0003_auto_20150528_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
