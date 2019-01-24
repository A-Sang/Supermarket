# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-24 16:20
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_activitymodel_bannermodel_zonemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zonemodel',
            options={'verbose_name': '专区管理', 'verbose_name_plural': '专区管理'},
        ),
        migrations.AlterField(
            model_name='goodsspumodel',
            name='spu_detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='详情'),
        ),
        migrations.AlterModelTable(
            name='zonemodel',
            table='活动专区表',
        ),
    ]