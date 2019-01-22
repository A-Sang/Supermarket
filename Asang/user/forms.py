from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from db.base_form import BaseModelForm
from user import hash_password
from user.models import User, UserInfo


# 注册form验证
class RegModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12,
                               min_length=8,
                               error_messages={'required': '密码不能为空',
                                               'max_length': '密码长度不能超过12位',
                                               'min_length': '密码长度不能小于8位'})
    repassword = forms.CharField(max_length=12,
                                 min_length=8,
                                 error_messages={'required': '密码不能为空',
                                                 'max_length': '密码长度不能超过12位',
                                                 'min_length': '密码长度不能小于8位'})
    checkbox = forms.BooleanField(error_messages={'required': '请查看用户协议'})
    captcha = forms.CharField(max_length=6,
                              strip=True,
                              error_messages={
                                  'required': "验证码必须填写"
                              })

    class Meta:
        model = User
        fields = ['phone_num']
        error_messages = {'phone_num': {'required': '手机号不能为空'}}

    # 验证手机是否已存在
    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        result = User.objects.filter(phone_num=phone_num).exists()
        if result:
            raise forms.ValidationError('该手机已注册')
        else:
            return phone_num

    # 验证两次密码是否相同
    def clean(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError({'repassword': '两次密码输入不一致'})
        try:
            phone=self.cleaned_data.get('phone_num')
            captcha=self.cleaned_data.get('captcha')
            r=get_redis_connection()
            random_code=r.get(phone)
            random_code=random_code.decode('utf-8')
            if random_code is None:
                raise forms.ValidationError({'captcha':'验证码失效,请重新获取验证码'})
            elif captcha and random_code !=captcha:
                raise forms.ValidationError({'captcha':'验证码输入错误!'})
        except:
            raise forms.ValidationError({'captcha':'验证码输入有误!'})
        return self.cleaned_data


# 登录验证
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_num', 'password']
        error_messages = {'phone_num': {'required': '账号不能为空',

                                        },
                          'password': {'required': '密码不能为空',
                                       }}

    def clean(self):
        phone_name = self.cleaned_data.get('phone_num')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(phone_num=phone_name)
        except User.DoesNotExist:
            raise forms.ValidationError({'phone_num': '账号不存在'})

        if user.password != hash_password(password):
            raise forms.ValidationError({'password': '账号或密码错误'})
        else:
            # 建立一个user对象到清洗数据上
            self.cleaned_data['user'] = user
            return self.cleaned_data

#修改密码验证
class NewpwdForm(forms.Form):
    password=forms.CharField(error_messages={'require':'密码未填写'},validators=[RegexValidator(r'\d{8,12}',message='输入8-12位密码')])
    new_password=forms.CharField(error_messages={'require':'新密码未填写'},validators=[RegexValidator(r'\d{8,12}',message='输入8-12位密码')])
    repassword=forms.CharField(error_messages={'require':'密码未填写'},validators=[RegexValidator(r'\d{8,12}',message='输入8-12位密码')])

    def check_password(self,request):
        id=request.session.get('id')
        password=hash_password(self.cleaned_data.get('password'))
        result=User.objects.filter(pk=id,password=password).exists()
        if result:
            return True
        else:
            self.add_error('password','密码输入错误')
            return False



    def clean(self):
        new_password=self.cleaned_data.get('new_password')
        repassword=self.cleaned_data.get('repassword')
        if new_password and repassword and new_password != repassword:
            raise forms.ValidationError({'repassword':'两次密码输入不一致'})
        else:
            self.add_error('password','密码输入错误')
            return

#忘记密码验证
class GetPasswordForm(RegModelForm):
    checkbox = None
    #基础注册form表单,重写手机号验证方法
    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        result = User.objects.filter(phone_num=phone_num).exists()
        if result:
            return phone_num
        else:
            raise forms.ValidationError('手机未注册,请注册')


#更换手机号验证
class PhoneForm(BaseModelForm):
    class Meta:
        model = User
        fields = ['phone_num']
        error_messages = {'phone_num': {'required': '手机号不能为空'}}

    # 验证手机是否已存在
    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        result = User.objects.filter(phone_num=phone_num).exists()
        if result:
            raise forms.ValidationError('该手机已注册')
        else:
            return phone_num



#更新个人信息验证
class InfoModelForm(forms.ModelForm):
    gender=forms.ChoiceField(choices=((1,'男'),(2,'女')))
    class Meta:
        model=UserInfo
        fields=['nickname','birthday','school','location','hometown']
        error_messages={'nickname':{'max_length': '昵称不能超过8个字符'},
                        'school':{'max_length': '不能超过20个字符'},
                        'location':{'max_length': '不能超过20个字符'},
                        'hometown':{'max_length': '不能超过20个字符'},
                        }