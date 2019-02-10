# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import provider.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=provider.utils.long_token, max_length=255, db_index=True)),
                ('expires', models.DateTimeField()),
                ('scope', models.IntegerField(default=2, choices=[(2, 'read'), (4, 'write'), (6, 'read+write')])),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(help_text="Your application's URL.")),
                ('redirect_uri', models.URLField(help_text="Your application's callback URL")),
                ('client_id', models.CharField(default=provider.utils.short_token, max_length=255)),
                ('client_secret', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('client_type', models.IntegerField(choices=[(0, 'Confidential (Web applications)'), (1, 'Public (Native and JS applications)')])),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='oauth2_client', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('expires', models.DateTimeField(default=provider.utils.get_code_expiry)),
                ('redirect_uri', models.CharField(max_length=255, blank=True)),
                ('scope', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=models.CASCADE, to='oauth2.Client')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('expired', models.BooleanField(default=False)),
                ('access_token', models.OneToOneField(on_delete=models.CASCADE, related_name='refresh_token', to='oauth2.AccessToken')),
                ('client', models.ForeignKey(on_delete=models.CASCADE, to='oauth2.Client')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='client',
            field=models.ForeignKey(on_delete=models.CASCADE, to='oauth2.Client'),
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
