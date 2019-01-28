import hashlib
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from django.http import JsonResponse

from django.shortcuts import redirect
from django_redis import get_redis_connection

from Asang.settings import SECRET_KEY, ACCESS_KEY_ID, ACCESS_KEY_SECRET

#密码加密
from goods.models import GoodsSKUModel


def hash_password(password):
    # 哈希,加盐
    for _ in range(3000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.sha256(pass_str.encode('utf-8'))
        password = h.hexdigest()
        return password

#设置session方法
def set_session(request, user):
    #设置session,验证没有id则返回登录页面
    request.session['id'] = user.pk
    request.session['phone_num']=user.phone_num
    #设置session过期时间,不填为两周,0为关闭浏览器过期,固定过期时间,None永不过期
    request.session.set_expiry(None)


# 检查session
def check_session(func):
    def new(request, *args, **kwargs):
        # 判断有没有session
        if request.session.get('id') is None:
            # 获取当前地址
            referer = request.META.get('HTTP_REFERER', None)
            if referer:
                # 如果有就添加到session中
                request.session['referer'] = referer
            # 判断是否是ajax请求is_ajax()返回布尔值
            if request.is_ajax():
                return JsonResponse(json_msg(4, '未登录'))
            else:
                return redirect('user:登录')
        else:
            # 如果有session调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
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

#设置Json格式数据
def json_msg(code,msg=None,data=None):
    """
    :param code:0 为正确，其他为错误
    :param msg: 错误信息
    :param data: 提交数据
    """
    return {'code':code,'errmsg':msg,'data':data}

#获取 当前用户购物车中的总数量
def get_count(request):

    user_id = request.session.get("id")
    if user_id is None:
        return 0
    else:
        # redis
        r = get_redis_connection()
        # 准备键
        cart_key = f"cart_{user_id}"
        # 获取字段值（多个）
        values = r.hvals(cart_key)
        # 准备一个总数量
        total_count = 0
        for v in values:
            total_count += int(v)
        return total_count


def get_price(request):
    # 获取参数
    user_id = request.session.get('id')
    # 拼接key
    cart_key = f"cart_{user_id}"
    # 操作数据库
    r = get_redis_connection()
    # 字典推导式遍历数据，返回sku对象和数量
    goods = {GoodsSKUModel.objects.get(pk=int(pk)): int(counts) for pk, counts in r.hgetall(cart_key).items()}
    # 推导式获取各个商品总价价格，返回列表
    price_list = [sku.price * count for sku, count in goods.items()]
    # for sku in goods.keys():
    #     price_list.append(sku.price)
    # 计算总价格
    total_price = 0
    for price in price_list:
        total_price += price
    return total_price