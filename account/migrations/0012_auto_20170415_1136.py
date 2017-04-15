# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_studentprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('lang', models.IntegerField(choices=[(1, 'A1 - Elementary'), (2, 'A2 - Pre-Intermediate'), (3, 'B1 - Intermediate'), (4, 'B2 - Upper intermediate'), (5, 'C1 - Advanced'), (6, 'C2 - Proficient')], default=1)),
            ],
            options={
                'managed': False,
                'db_table': 'account_student',
            },
        ),
        migrations.RemoveField(
            model_name='student_fram',
            name='show',
        ),
        migrations.RemoveField(
            model_name='student_lang',
            name='show',
        ),
        migrations.RemoveField(
            model_name='student_other',
            name='show',
        ),
    ]
