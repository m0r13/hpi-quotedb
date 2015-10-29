# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedb', '0004_quote_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='voting',
            field=models.IntegerField(default=0),
        ),
    ]
