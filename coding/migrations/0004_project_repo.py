# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0003_auto_20150622_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='repo',
            field=models.URLField(null=True, verbose_name=b'Repository', blank=True),
        ),
    ]
