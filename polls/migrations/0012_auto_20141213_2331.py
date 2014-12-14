# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0011_auto_20141213_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='down_list',
            field=models.ManyToManyField(related_name='down_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answers',
            name='up_list',
            field=models.ManyToManyField(related_name='up_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
