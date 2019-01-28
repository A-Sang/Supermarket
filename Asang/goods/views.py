from django.http import HttpResponse
from django.shortcuts import render
from django.views import View



# Create your views here.
from db.helper import get_count
from goods.models import BannerModel, ZoneModel, GoodsSKUModel, GoodsSPUModel, CategoryModel


class IndexView(View):
    #主页
    def get(self,request):
        banner=BannerModel.objects.filter(is_del=False)
        zones=ZoneModel.objects.filter(is_online=True)
        context={'banner':banner,'zones':zones}
        return render(request,'goods/index.html',context=context)

    def post(self,request):
        return HttpResponse('OK')

class DetailView(View):
    #详情页
    def get(self,request,id):
        sku=GoodsSKUModel.objects.get(id=id)
        context={'sku':sku,}
        return render(request,'goods/detail.html',context=context)

    def post(self,request):
        return HttpResponse('OK')


class CateGoryView(View):
    #列表页
    def get(self, request,id,order):
        #查询所有分类
        categorys=CategoryModel.objects.filter(is_del=False)

        if id =='':
            #正则中*接收0或多个,当为0时返回空字符串
            cate=categorys.first()
            #默认为分类中的第一个
            id=cate.id

        #接收到的id为字符串,要转化为int,用于比较
        id=int(id)
        category=CategoryModel.objects.get(pk=id)
        #查询分类对应的商品
        goods=GoodsSKUModel.objects.filter(is_del=False,category=category)
        """
        设置对应商品排序字段:销量,价格(降,升),添加时间,综合(pk)
        设置传入对应参数:0:综合,1:销量,2:价格(升),3:价格(降),4:添加时间
        将字段放进列表中,参数为其所对应的索引
        """

        order_rule=['pk','-sales','price','-price','-create_time']
        if order == '':
            #接收空字符时默认为0
            order=0
        #接收的参数为字符串,需转化为整数,用于判断
        order = int(order)
        #根据接收的参数索引,对应排序查询
        goods=goods.order_by(order_rule[order])
        # 获取购物车总数量
        count_cart = get_count(request)
        context={'categorys':categorys,
                 "goods":goods,
                 'id':id,
                 'order':order,
                 'count_cart':count_cart}
        return render(request, 'goods/category.html',context=context)

    def post(self, request):
        return HttpResponse('OK')
