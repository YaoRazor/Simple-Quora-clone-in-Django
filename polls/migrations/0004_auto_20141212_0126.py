# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20141211_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='votes',
            new_name='up_votes',
        ),
        migrations.AddField(
            model_name='answers',
            name='down_votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
