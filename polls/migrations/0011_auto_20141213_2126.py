# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20141213_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='modification_time',
            field=models.DateTimeField(verbose_name=b'date modified'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='modification_time',
            field=models.DateTimeField(verbose_name=b'date modified'),
            preserve_default=True,
        ),
    ]
