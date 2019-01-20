from django import forms

from user import hash_password
from user.models import User


# 注册form验证
class RegModelForm(forms.ModelForm):
    password = forms.CharField(max_length=12,
                               min_length=8,
                               error_messages={'required': '密码不能未空',
                                               'max_length': '密码长度不能超过12位',
                                               'min_length': '密码长度不能小于8位'})
    repassword = forms.CharField(max_length=12,
                                 min_length=8,
                                 error_messages={'required': '密码不能未空',
                                                 'max_length': '密码长度不能超过12位',
                                                 'min_length': '密码长度不能小于8位'})
    checkbox = forms.BooleanField(error_messages={'required': '请查看用户协议'})

    class Meta:
        model = User
        fields = ['phone_num']
        error_messages = {'phone_num': {'required': '手机号不能未空'}}

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
        else:
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
