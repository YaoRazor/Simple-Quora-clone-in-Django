# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20141213_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='modification_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 2, 23, 10, 856281, tzinfo=utc), verbose_name=b'date modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modification_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 2, 23, 10, 855222, tzinfo=utc), verbose_name=b'date modified'),
            preserve_default=True,
        ),
    ]
