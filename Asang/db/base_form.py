from django import forms

#验证验证码是否正确
from django_redis import get_redis_connection


class BaseForm(forms.Form):
    captcha = forms.CharField(max_length=6,
                              strip=True,
                              error_messages={
                                  'required': "验证码必须填写"
                              })
    def clean(self):
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


class BaseModelForm(forms.ModelForm):
    captcha = forms.CharField(max_length=6,
                              strip=True,
                              error_messages={
                                  'required': "验证码必须填写"
                              })
    def clean(self):
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
