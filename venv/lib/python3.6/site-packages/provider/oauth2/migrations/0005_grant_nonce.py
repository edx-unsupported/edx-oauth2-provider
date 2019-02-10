# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2', '0004_add_index_on_grant_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='grant',
            name='nonce',
            field=models.CharField(default='', max_length=255, blank=True),
        ),
    ]
