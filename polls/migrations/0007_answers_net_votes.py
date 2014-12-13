# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20141213_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='net_votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
