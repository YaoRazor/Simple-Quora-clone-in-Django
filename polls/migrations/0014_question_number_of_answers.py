# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20141214_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='number_of_answers',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
