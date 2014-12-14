# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0012_auto_20141213_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='down_list',
            field=models.ManyToManyField(related_name='question_down_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='down_votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='up_list',
            field=models.ManyToManyField(related_name='question_up_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='up_votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answers',
            name='down_list',
            field=models.ManyToManyField(related_name='answer_down_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='answers',
            name='up_list',
            field=models.ManyToManyField(related_name='answer_up_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
