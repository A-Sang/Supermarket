from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from db.base_view import BaseView
from user import hash_password, set_session, check_session
from user.forms import RegModelForm, LoginModelForm
from user.models import User
# Create your views here.





#个人中心
@check_session
def member(request):
    return render(request,'user/member.html')

#安全设置
@check_session
def saftystep(request):
    return render(request, 'user/saftystep.html')


# 登录
class LoginView(View):
        #get请求展示登录页面
    def get(self, request):
        return render(request, 'user/login.html')
        #post请求,获取参数进行验证
    def post(self, request):
        data=request.POST
        form=LoginModelForm(data)
        if form.is_valid():
            user=form.cleaned_data.get('user')
            set_session(request,user)
            #验证成功跳转登录中心
            return redirect('user:个人中心')
        else:
            context={'data':data,
                     'error':form.errors}
            return render(request,'user/login.html',context=context)

#注册
class RegisterView(View):
    # get请求展示登录页面
    def get(self, request):
        return render(request, 'user/reg.html')

    # post请求,获取参数进行验证
    def post(self, request):
        data=request.POST
        form=RegModelForm(data)
        if form.is_valid():
            user=User()
            user.phone_num=form.cleaned_data.get('phone_num')
            user.password=hash_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('user:登录')
        else:
            context={'data':data,
                     'error':form.errors}
            return render(request,'user/reg.html',context=context)

#设置新密码
class NewPwdView(View):

    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        return HttpResponse('200')

#忘记密码
class ForPwdView(View):

    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        return HttpResponse('200')

#绑定新手机号
class BoundPhoneView(BaseView):

    def get(self, request):
        return render(request, 'user/boundphone.html')

    def post(self, request):
        return HttpResponse('200')

#设置支付密码
class PaymentView(BaseView):

    def get(self, request):
        return render(request, 'user/payment.html')

    def post(self, request):
        return HttpResponse('200')

#地址管理
class GiAddressView(BaseView):

    def get(self,request):
        return render(request,'user/gladdress.html')

    def post(self,request):
        return HttpResponse('200')
#编辑地址
class EditAddressView(BaseView):

    def get(self,request):
        return render(request,'user/editaddress.html')

    def post(self,request):
        return HttpResponse('200')

#删除地址
@check_session
def delete(request):
    return HttpResponse('200')


#添加地址
class AddressView(BaseView):

    def get(self,request):
        return render(request,'user/address.html')

    def post(self,request):
        return HttpResponse('200')


#个人信息
class InfoView(BaseView):

    def get(self,request):
        return render(request,'user/infor.html')

    def post(self,request):
        return HttpResponse("200")