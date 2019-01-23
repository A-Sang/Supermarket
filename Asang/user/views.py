import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection
from db.base_view import BaseView
from user import hash_password, set_session, check_session, send_sms
from user.forms import RegModelForm, LoginModelForm, NewpwdForm, GetPasswordForm, PhoneForm, InfoModelForm
from user.models import User, UserInfo


# Create your views here.


# 个人中心
@check_session
def member(request):
    phone = request.session.get('phone_num')
    user=UserInfo.objects.get(pk=request.session.get('id'))
    return render(request, 'user/member.html',{'phone':phone,'user':user})


# 安全设置
@check_session
def saftystep(request):
    phone=request.session.get('phone_num')
    return render(request, 'user/saftystep.html',{'phone':phone})


# 登录
class LoginView(View):

    def get(self, request):
        # get请求展示登录页面
        return render(request, 'user/login.html')

    # post请求,获取参数进行验证
    def post(self, request):
        data = request.POST
        form = LoginModelForm(data)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            # 设置session
            set_session(request, user)
            # 验证成功跳转登录中心
            return redirect('user:个人中心')
        else:
            context = {'data': data,
                       'form': form}
            return render(request, 'user/login.html', context=context)


# 注册
class RegisterView(View):

    def get(self, request):
        # get请求展示登录页面
        return render(request, 'user/reg.html')

    # post请求,获取参数进行验证
    def post(self, request):
        data = request.POST
        form = RegModelForm(data)
        if form.is_valid():
            # 验证通过保存数据,并跳转到登录页面
            user = User()
            user.phone_num = form.cleaned_data.get('phone_num')
            user.password = hash_password(form.cleaned_data.get('password'))
            user.save()
            #添加一对一用户信息表
            id=User.objects.get(phone_num=form.cleaned_data.get('phone_num')).pk
            UserInfo.objects.create(user_id=id)
            return redirect('user:登录')
        else:
            # 验证失败返回提示错误信息
            return render(request, 'user/reg.html', {'form':form})


# 设置新密码
class NewPwdView(BaseView):

    def get(self, request):
        # get请求展示页面
        id=request.session.get('id')
        return render(request, 'user/password.html',{'id':id})

    def post(self, request):
        #验证提交数据是否合法
        # 如果接收session中的id
        id = request.session.get('id')
        data=request.POST
        form=NewpwdForm(data)
        if form.is_valid():
            if form.check_password(request):
                #对新密码加密
                new_password=hash_password(form.cleaned_data.get('new_password'))
                # 通过id更新对应用户密码
                User.objects.filter(id=id).update(password=new_password)
                return redirect('user:个人中心')
            else:
                context = {'data': data,
                           'form': form,
                           }
                return render(request, 'user/password.html', context=context)

        else:
            context={'data':data,
                     'form':form,
                     }
            return render(request,'user/password.html',context=context)




# 忘记密码
class ForPwdView(View):

    def get(self, request):
        #get请求展示页面
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        #post请求获取参数
        data=request.POST
        form=GetPasswordForm(data)
        if form.is_valid():
            #操作数据库,根据手机号更改新密码
            phone_num=form.cleaned_data.get('phone_num')
            password=hash_password(form.cleaned_data.get('password'))
            User.objects.filter(phone_num=phone_num).update(password=password)
            return redirect('user:登录')
        else:
            context={'form':form}
            return render(request,'user/forgetpassword.html',context=context)


# 绑定新手机号
class BoundPhoneView(BaseView):

    def get(self, request):
        #get请求展示页面
        return render(request, 'user/boundphone.html')

    def post(self, request):
        id=request.session.get('id')
        data=request.POST
        form=PhoneForm(data)
        if form.is_valid():
            phone_num=form.cleaned_data.get('phone_num')
            User.objects.filter(id=id).update(phone_num=phone_num)
            return redirect('user:个人中心')
        else:
            context={'data':data,
                     'form':form}
            return render(request,'user/boundphone.html',context=context)



# 设置支付密码
class PaymentView(BaseView):

    def get(self, request):
        return render(request, 'user/payment.html')

    def post(self, request):
        return HttpResponse('200')


# 地址管理
class GiAddressView(BaseView):

    def get(self, request):
        return render(request, 'user/gladdress.html')

    def post(self, request):
        return HttpResponse('200')


# 编辑地址
class EditAddressView(BaseView):

    def get(self, request):
        return render(request, 'user/editaddress.html')

    def post(self, request):
        return HttpResponse('200')


# 删除地址
@check_session
def delete(request):
    return HttpResponse('200')


# 添加地址
class AddressView(BaseView):

    def get(self, request):
        return render(request, 'user/address.html')

    def post(self, request):
        return HttpResponse('200')


# 个人信息
class InfoView(BaseView):

    def get(self, request):
        id=request.session.get('id')
        user=User.objects.get(id=id)
        data=UserInfo.objects.get(user_id=id)
        context={'data':data,'user':user}
        return render(request, 'user/infor.html',context=context)

    def post(self, request):
        id=request.session.get('id')
        data=request.POST
        form=InfoModelForm(data)
        info = UserInfo.objects.get(pk=id)
        info.head=request.FILES.get('head')
        info.save()
        if form.is_valid():
            info.nickname=form.cleaned_data.get('nickname')
            info.birthday=form.cleaned_data.get('birthday')
            info.gender=form.cleaned_data.get('gender')
            info.school=form.cleaned_data.get('school')
            info.location=form.cleaned_data.get('location')
            info.hometown=form.cleaned_data.get('hometown')
            info.save()
            return redirect('user:个人中心')
        else:
            return render(request,'user/infor.html')

#发送短信验证码
class SendMsm(View):
    #get请求
    def get(self,request):
        pass

    def post(self,request):
        #获取参数
        phone=request.POST.get('phone_num',"")
        rs=re.search('^1[3-9]\d{9}$',phone)
        if rs is None:
            return JsonResponse({'error':1,'errmsg':'手机格式错误!'})
        #生成随机验证码
        random_code="".join([str(random.randint(0,9)) for _ in range(6)])
        print("============={}===========".format(random_code))
        #获取redis链接
        r= get_redis_connection()
        r.set(phone,random_code)
        #设置验证码2分钟后过期
        r.expire(phone,120)
        #设置获取验证码次数
        key_times="{}_times".format(phone)
        #获取手机当前发送验证码次数
        now_time=r.get(key_times)
        if now_time is None or int(now_time) < 5:
            #判断获取次数,redis获取值为二进制,要转码
            r.incr(key_times)
            #每使用一次+1
            r.expire(key_times,3600)
            #设置1个小时后再重新获取验证码
        else:
            return JsonResponse({'error':1,'errmsg':'获取超过限制,1小时后再来'})
        #链接第三方
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"阿桑证券\"}" % random_code
        # print(params)
        rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        return JsonResponse({'error':0})
