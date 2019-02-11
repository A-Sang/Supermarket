from django.db import models

# Create your models here.
from db.base_model import BaseModel


# 运输公司模型
class TranSport(BaseModel):
    name = models.CharField(max_length=50, verbose_name='运输公司')
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0, verbose_name='运输价格')

    def __str__(self):
        return self.name

    class Meta:
        db_table = '运输公司'
        verbose_name = '运输公司'
        verbose_name_plural = verbose_name


class Payment(BaseModel):
    name = models.CharField(max_length=50, verbose_name="支付方式")
    brief = models.CharField(max_length=200, verbose_name="说明")
    logo = models.ImageField(upload_to="payment/%Y", verbose_name="支付LOGO")

    def __str__(self):
        return self.name

    class Meta:
        db_table = '支付方式'
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name


# 订单基本信息
class Oder(BaseModel):
    order_status_choices = (
        (0, "未支付"),
        (1, "已支付"),
        (2, "已发货"),
        (3, "未评价"),
        (4, "已完成"),
        (5, "退发货"),
        (6, "取消订单"),
    )
    username = models.CharField(max_length=100, verbose_name='收货人')
    number = models.CharField(max_length=64, verbose_name='订单编号')
    phone = models.CharField(max_length=11, verbose_name='收货人电话')
    address = models.CharField(max_length=200, verbose_name='收货地址')
    transport = models.CharField(max_length=50, verbose_name='运输方式')
    order_price = models.DecimalField(decimal_places=2, max_digits=9, default=0, verbose_name='订单金额')
    transport_price = models.DecimalField(decimal_places=2, max_digits=9, default=0, verbose_name='运费')
    pay_money = models.DecimalField(decimal_places=2, max_digits=9, default=0, verbose_name='实付金额')
    order_status = models.SmallIntegerField(choices=order_status_choices, default=0, verbose_name='订单状态')
    user = models.ForeignKey(to='user.UserInfo', verbose_name='用户')
    payment = models.ForeignKey(to='Payment',null=True, blank=True, verbose_name='支付方式')
    comment=models.TextField(null=True,blank=True,verbose_name='备注')
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True, blank=True)
    deliver_time = models.DateTimeField(verbose_name="发货时间", null=True, blank=True)
    finish_time = models.DateTimeField(verbose_name="完成时间", null=True, blank=True)

    def __str__(self):
        return self.number

    class Meta:
        db_table = '订单基本表'
        verbose_name = "订单基本信息"
        verbose_name_plural = verbose_name


# 订单详情
class OrderGoods(BaseModel):
    order = models.ForeignKey(to="Oder", verbose_name="订单ID")
    goods_sku = models.ForeignKey(to="goods.GoodsSKUModel", verbose_name="订单商品ID")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="商品价格")
    count = models.SmallIntegerField(verbose_name="订单商品数量")

    def __str__(self):
        return "{}:{}".format(self.order.number, self.goods_sku.sku_name)

    class Meta:
        db_table = '订单详情表'
        verbose_name = "订单商品信息"
        verbose_name_plural = verbose_name
