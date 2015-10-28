# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.IntegerField(default=1)),
                ('quote', models.ForeignKey(to='quotedb.Quote')),
            ],
        ),
        migrations.CreateModel(
            name='VoteKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('key', models.CharField(blank=True, max_length=255, default='')),
            ],
        ),
    ]
