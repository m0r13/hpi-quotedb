# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedb', '0005_quote_voting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='tags',
            field=models.ManyToManyField(to='quotedb.Tag'),
        ),
    ]
