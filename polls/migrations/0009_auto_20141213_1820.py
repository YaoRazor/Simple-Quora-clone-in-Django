# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_question_modification_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='modification_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 23, 20, 26, 939395, tzinfo=utc), verbose_name=b'date modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modification_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 23, 20, 26, 937869, tzinfo=utc), verbose_name=b'date modified'),
            preserve_default=True,
        ),
    ]
