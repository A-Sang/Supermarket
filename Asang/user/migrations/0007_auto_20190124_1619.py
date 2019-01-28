# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-24 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190123_1139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '用户账号管理'},
        ),
        migrations.AlterModelOptions(
            name='useraddress',
            options={'verbose_name_plural': '用户地址管理'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '用户信息管理'},
        ),
        migrations.AlterModelTable(
            name='user',
            table='用户表',
        ),
        migrations.AlterModelTable(
            name='useraddress',
            table='用户地址表',
        ),
        migrations.AlterModelTable(
            name='userinfo',
            table='用户信息表',
        ),
    ]