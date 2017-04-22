# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 20:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20170422_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='github',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='group',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='validated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validate_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
