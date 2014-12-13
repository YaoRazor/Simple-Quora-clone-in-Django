# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20141212_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 3, 16, 33, 615162, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
