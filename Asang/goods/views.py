from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):

    def get(self,request):
        return render(request,'goods/index.html')

    def post(self,request):
        return HttpResponse('OK')

class DetailView(View):

    def get(self,request):
        return render(request,'goods/detail.html')

    def post(self,request):
        return HttpResponse('OK')

class ListView(View):

    def get(self,request):
        return render(request,'goods/list.html')

    def post(self,request):
        return HttpResponse('OK')


class CateGoryView(View):

    def get(self, request):
        return render(request, 'goods/category.html')

    def post(self, request):
        return HttpResponse('OK')
