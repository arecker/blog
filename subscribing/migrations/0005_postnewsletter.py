# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0006_auto_20150523_2127'),
        ('subscribing', '0004_auto_20150529_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostNewsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_created=True)),
                ('send_on_save', models.BooleanField(default=False, verbose_name=b'Send on Save')),
                ('post', models.ForeignKey(to='blogging.Post')),
            ],
        ),
    ]
