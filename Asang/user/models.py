from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class User(BaseModel):
    phone_num = models.CharField(max_length=11, verbose_name='登录手机号', validators=[RegexValidator(regex=r'^1[3-9]\d{9}$',
                                                                                                 message='请输入有效手机号码')])
    password = models.CharField(max_length=64, verbose_name='登录密码')

    def __str__(self):
        return self.phone_num

    class Meta:
        db_table = '用户表'
        verbose_name_plural = '用户账号管理'


class UserInfo(BaseModel):
    choices = ((1, '男'), (2, '女'))
    nickname = models.CharField(max_length=8, verbose_name='昵称', null=True, blank=True)
    gender = models.SmallIntegerField(choices=choices, default=1, verbose_name='性别')
    birthday = models.DateField(null=True, verbose_name='生日', blank=True)
    school = models.CharField(max_length=20, null=True, verbose_name='学校', blank=True)
    location = models.CharField(max_length=20, null=True, verbose_name='住址', blank=True)
    hometown = models.CharField(max_length=20, null=True, verbose_name='籍贯', blank=True)
    paypassword = models.CharField(max_length=64, null=True, verbose_name='支付密码', blank=True)
    user = models.OneToOneField(to='User', primary_key=True, verbose_name='ID', blank=True)
    head = models.ImageField(upload_to='head/%Y%m/', default='/head/infortx.png', verbose_name='头像')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = '用户信息表'
        verbose_name_plural = '用户信息管理'


class UserAddress(BaseModel):
    name = models.CharField(max_length=10, verbose_name='收货人')
    phone_num = models.CharField(max_length=11, verbose_name='联系电话',validators=[RegexValidator('^1[3-9]\d{9}$',
                                                                                               message='手机格式错误！')])
    hcity = models.CharField(max_length=10, verbose_name='省')
    hproper = models.CharField(max_length=10, verbose_name='区/县')
    harea = models.CharField(max_length=10, verbose_name='区/县')
    brief = models.CharField(max_length=20, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    userinfo = models.ForeignKey(to='UserInfo')

    def __str__(self):
        return self.name

    class Meta:
        db_table = '用户地址表'
        verbose_name = '用户地址管理'
        verbose_name_plural = verbose_name


class UserBuy(models.Model):
    pass
