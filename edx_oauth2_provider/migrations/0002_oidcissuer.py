# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2', '0001_initial'),
        ('edx_oauth2_provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OidcIssuer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('client', models.ForeignKey(related_name='oidc_issuer', to='oauth2.Client')),
            ],
            options={
                'db_table': 'oauth2_provider_oidc_issuer',
            },
        ),
    ]
