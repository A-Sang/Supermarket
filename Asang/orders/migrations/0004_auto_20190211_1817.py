# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-11 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190211_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oder',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Payment', verbose_name='支付方式'),
        ),
    ]
