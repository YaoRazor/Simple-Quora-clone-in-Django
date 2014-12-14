# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_answers_net_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='modification_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 23, 3, 37, 136284, tzinfo=utc), verbose_name=b'date modified'),
            preserve_default=True,
        ),
    ]
