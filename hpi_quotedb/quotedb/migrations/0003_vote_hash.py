# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedb', '0002_vote_votekey'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='hash',
            field=models.CharField(blank=True, max_length=255, default=''),
        ),
    ]
