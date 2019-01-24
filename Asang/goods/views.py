from django.http import HttpResponse
from django.shortcuts import render
from django.views import View



# Create your views here.
from goods.models import BannerModel, ZoneModel, GoodsSKUModel, GoodsSPUModel, CategoryModel


class IndexView(View):

    def get(self,request):
        banner=BannerModel.objects.all()
        zones=ZoneModel.objects.all()
        context={'banner':banner,'zones':zones}
        return render(request,'goods/index.html',context=context)

    def post(self,request):
        return HttpResponse('OK')

class DetailView(View):

    def get(self,request,id):
        sku=GoodsSKUModel.objects.get(id=id)
        context={'sku':sku,}
        return render(request,'goods/detail.html',context=context)

    def post(self,request):
        return HttpResponse('OK')


class CateGoryView(View):

    def get(self, request,id):
        gate=CategoryModel.objects.all()
        goods=CategoryModel.objects.get(pk=id)
        gate_list=goods.goodsskumodel_set.all()
        context={'gate':gate,"gate_list":gate_list}
        return render(request, 'goods/category.html',context=context)

    def post(self, request):
        return HttpResponse('OK')
