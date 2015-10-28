# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedb', '0003_vote_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
