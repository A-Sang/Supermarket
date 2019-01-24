# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否注销')),
                ('title', models.CharField(max_length=200, verbose_name='活动名')),
                ('img_url', models.ImageField(upload_to='activity/%Y/%m/%d', verbose_name='活动图片相册')),
                ('url_site', models.URLField(verbose_name='活动链接')),
            ],
            options={
                'verbose_name': '活动管理',
                'verbose_name_plural': '活动管理',
                'db_table': '活动表',
            },
        ),
        migrations.CreateModel(
            name='BannerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否注销')),
                ('name', models.CharField(max_length=100, verbose_name='轮播活动名')),
                ('img_url', models.ImageField(upload_to='banner/%Y/%m/%d', verbose_name='轮播相册')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSKUModel', verbose_name='SKU商品名')),
            ],
            options={
                'verbose_name': '轮播活动管理',
                'verbose_name_plural': '轮播活动管理',
                'db_table': '轮播表',
            },
        ),
        migrations.CreateModel(
            name='ZoneModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否注销')),
                ('title', models.CharField(max_length=100, verbose_name='专区名')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='活动介绍')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_online', models.BooleanField(choices=[(True, '上线'), (False, '下线')], default=False, verbose_name='是否上线')),
                ('sku', models.ManyToManyField(to='goods.GoodsSKUModel', verbose_name='SKU商品名')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
