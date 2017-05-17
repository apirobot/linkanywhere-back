# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-17 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]