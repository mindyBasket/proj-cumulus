# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-20 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flipbooks', '0010_auto_20170920_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scene',
            name='order_list',
        ),
        migrations.AddField(
            model_name='scene',
            name='children_orders',
            field=models.TextField(default='', max_length=200),
        ),
    ]
