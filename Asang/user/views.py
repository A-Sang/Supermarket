from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from user import hash_password
# Create your views here.





#个人中心
def member(request):
    return render(request,'user/member.html')

#安全设置
def saftystep(request):
    return render(request, 'user/saftystep.html')


# 登录
#@hash_password
class LoginView(View):

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        return HttpResponse('200')

#注册
#@hash_password
class RegisterView(View):

    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        return redirect('user:登录')

#设置新密码
#@hash_password
class NewPwdView(View):

    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        return HttpResponse('200')

#忘记密码
#@hash_password
class ForPwdView(View):

    def get(self, request):
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        return HttpResponse('200')

#绑定新手机号
class BoundPhoneView(View):

    def get(self, request):
        return render(request, 'user/boundphone.html')

    def post(self, request):
        return HttpResponse('200')

#设置支付密码
#@hash_password
class PaymentView(View):

    def get(self, request):
        return render(request, 'user/payment.html')

    def post(self, request):
        return HttpResponse('200')

#地址管理
class GiAddressView(View):

    def get(self,request):
        return render(request,'user/gladdress.html')

    def post(self,request):
        return HttpResponse('200')
#编辑地址
class EditAddressView(View):

    def get(self,request):
        return render(request,'user/editaddress.html')

    def post(self,request):
        return HttpResponse('200')

#删除地址
def delete(request):
    return HttpResponse('200')


#添加地址
class AddressView(View):

    def get(self,request):
        return render(request,'user/address.html')

    def post(self,request):
        return HttpResponse('200')


#个人信息
class InfoView(View):

    def get(self,request):
        return render(request,'user/infor.html')

    def post(self,request):
        return HttpResponse("200")