from django.db import models

# Create your models here.
from db.base_model import BaseModel


class CategoryModel(BaseModel):

    category_name=models.CharField(max_length=100,verbose_name='商品分类名')

    def __str__(self):
        return self.category_name

    class Meta:
        db_table='商品分类表'
        verbose_name='商品分类管理'
        verbose_name_plural=verbose_name

class UnitModel(BaseModel):

    unit_name=models.CharField(max_length=10,verbose_name='单位')

    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = '单位表'
        verbose_name = '单位管理'
        verbose_name_plural = verbose_name

class GoodsSPUModel(BaseModel):

    spu_name=models.CharField(max_length=100,verbose_name='SPU名')
    spu_detail=models.TextField(verbose_name='详情')

    def __str__(self):
        return self.spu_name

    class Meta:
        db_table = 'SPU商品表'
        verbose_name = 'SPU商品管理'
        verbose_name_plural = verbose_name

class GoodsSKUModel(BaseModel):

    spu = models.ForeignKey(to=GoodsSPUModel, verbose_name='SPU商品名')
    sku_name=models.CharField(max_length=100,verbose_name='SKU商品名')
    introduction=models.CharField(max_length=200,verbose_name='简介')
    price=models.DecimalField(max_digits=9,decimal_places=2,default=0,verbose_name='单价')
    unit = models.ForeignKey(to=UnitModel, verbose_name='单位')
    stock=models.IntegerField(default=0,verbose_name='库存')
    sales=models.IntegerField(default=0,verbose_name='销量')
    LOGO=models.ImageField(verbose_name='封面地址',upload_to='goods/%Y/%m/d')
    is_sale=models.BooleanField(default=False,choices=((True,'上架'),(False,'下架')),verbose_name='是否上架')
    category=models.ForeignKey(to=CategoryModel,verbose_name='类别')

    def __str__(self):
        return self.sku_name

    class Meta:
        db_table='SKU商品表'
        verbose_name='SKU商品管理'
        verbose_name_plural='SKU商品管理'

class GalleryModel(BaseModel):

    img_url=models.ImageField(verbose_name='商品相册',upload_to='goods_gallery/%Y/%m/%d')
    sku=models.ForeignKey(to=GoodsSKUModel,verbose_name='SKU商品名')
    def __str__(self):
        return '商品相册:{}'.format(self.img_url.name)

    class Meta:
        db_table='商品相册表'
        verbose_name='商品相册管理'
        verbose_name_plural=verbose_name


class BannerModel(BaseModel):

    name=models.CharField(max_length=100,verbose_name='轮播活动名')
    sku=models.ForeignKey(to=GoodsSKUModel,verbose_name='SKU商品名')
    img_url=models.ImageField(verbose_name='轮播相册',upload_to='banner/%Y/%m/%d')
    order=models.SmallIntegerField(default=0,verbose_name='排序')

    def __str__(self):
        return self.name

    class Meta:
        db_table='轮播表'
        verbose_name='轮播活动管理'
        verbose_name_plural=verbose_name

class ActivityModel(BaseModel):

    title=models.CharField(max_length=200,verbose_name='活动名')
    img_url=models.ImageField(verbose_name='活动图片相册',upload_to='activity/%Y/%m/%d')
    url_site=models.URLField(max_length=200,verbose_name='活动链接')

    def __str__(self):
        return self.title

    class Meta:
        db_table='活动表'
        verbose_name='活动管理'
        verbose_name_plural=verbose_name

class ZoneModel(BaseModel):
    title=models.CharField(max_length=100,verbose_name='专区名')
    brief=models.CharField(max_length=200,null=True,blank=True,verbose_name='活动介绍')
    order=models.SmallIntegerField(default=0,verbose_name='排序')
    is_online=models.BooleanField(default=False,choices=((True,'上线'),(False,'下线')),verbose_name='是否上线')
    sku=models.ManyToManyField(to=GoodsSKUModel,verbose_name='SKU商品名')
