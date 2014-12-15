# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('modification_time', models.DateTimeField(verbose_name=b'date modified')),
                ('up_votes', models.IntegerField(default=0)),
                ('down_votes', models.IntegerField(default=0)),
                ('net_votes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('down_list', models.ManyToManyField(related_name='answer_down_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=1000)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('modification_time', models.DateTimeField(verbose_name=b'date modified')),
                ('up_votes', models.IntegerField(default=0)),
                ('down_votes', models.IntegerField(default=0)),
                ('number_of_answers', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('down_list', models.ManyToManyField(related_name='question_down_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='polls.Tags', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='up_list',
            field=models.ManyToManyField(related_name='question_up_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(to='polls.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answers',
            name='up_list',
            field=models.ManyToManyField(related_name='answer_up_list', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
