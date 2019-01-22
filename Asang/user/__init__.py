import hashlib
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

from django.shortcuts import redirect

from Asang.settings import SECRET_KEY, ACCESS_KEY_ID, ACCESS_KEY_SECRET


def hash_password(password):
    # 哈希,加盐
    for _ in range(3000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.sha256(pass_str.encode('utf-8'))
        password = h.hexdigest()
        return password


def set_session(request, user):
    #设置session,验证没有id则返回登录页面
    request.session['id'] = user.pk
    request.session['phone_num']=user.phone_num
    #设置session过期时间,不填为两周,0为关闭浏览器过期,固定过期时间,None永不过期
    request.session.set_expiry(None)


def check_session(func):
    def new (request,*args,**kwargs):
        if request.session.get('id') is None:
            return redirect('user:登录')
        else:
            #如果有session调用原函数
            return func(request,*args,**kwargs)
    #返回新函数
    return new



# 完成 定义一个方法 发送短消
# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse