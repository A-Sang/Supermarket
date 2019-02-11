import random
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import BaseView
from db.helper import check_session, json_msg
from goods.models import GoodsSKUModel
from orders.models import TranSport, OrderGoods, Oder, Payment
from user.models import UserAddress, UserInfo

"""订单列表"""
@check_session
def orderlist(request):
    orders=Oder.objects.all()
    context={'orders':orders}
    return render(request, 'orders/allorder.html',context=context)


"""确认订单页面"""
@check_session
def tureorder(request):
    # 获取用户地址
    user_id = request.session.get('id')
    address = UserAddress.objects.filter(userinfo_id=user_id, is_del=False).order_by('-is_default').first()
    # 获取数据
    sku_ids = request.GET.getlist('sku_ids')
    goods_skus = []
    total_price = 0
    # 链接redis
    r = get_redis_connection()
    cart_key = f'cart_{user_id}'
    for sku_id in sku_ids:
        # 判断商品是否下架，如果下架返回购物车列表
        try:
            goods_sku = GoodsSKUModel.objects.get(pk=sku_id, is_del=False, is_sale=True)
        except GoodsSKUModel.DoesNotExist:
            return redirect('shopcart:购物车')
        # 获取购物车数量
        count = r.hget(cart_key, sku_id)
        count = int(count)
        # 将数量对象添加到sku商品对象上
        goods_sku.count = count
        goods_skus.append(goods_sku)
        # 计算商品总价格
        total_price += goods_sku.price * count
        # 获取运输方式对象
        transports = TranSport.objects.filter(is_del=False).order_by('price')

    context = {'address': address,
               'goods_skus': goods_skus,
               'total_price': total_price,
               'transports': transports}
    return render(request, 'orders/tureorder.html', context=context)


"""保存订单"""
@check_session
def save_order(request):
    # 获取数据
    user_id = request.session.get('id')
    transport_id = request.POST.get('transport')
    sku_ids = request.POST.getlist('sku_ids')
    address_id = request.POST.get('address_id')
    comment = request.POST.get('comment')
    # 验证数据合法性
    try:
        transport_id = int(transport_id)
        address_id = int(address_id)
        sku_ids = [int(sku_id) for sku_id in sku_ids]
    except:
        return JsonResponse(json_msg(1, '参数错误'))
    # 只需再确认地址和运输方式是否存在
    try:
        transport = TranSport.objects.get(pk=transport_id)
    except TranSport.DoesNotExist:
        return JsonResponse(json_msg(2, '运输方式不存在'))
    try:
        address = UserAddress.objects.get(pk=address_id)
    except UserAddress.DoesNotExist:
        return JsonResponse(json_msg(3, '收货地址不存在'))
    # 数据合法，操作数据库保存数据
    # 拼接订单编号
    number = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
    # 拼接收货地址
    addressinfo = "{}{}{}--{}".format(address.hcity, address.hproper, address.harea, address.brief)
    user = UserInfo.objects.get(pk=user_id)
    # 创建订单基本信息,订单金额和实际实付金额后面保存，订单状态默认为未支付，支付方式在支付页面保存
    order = Oder.objects.create(username=address.name,
                                number=number,
                                phone=address.phone_num,
                                address=addressinfo,
                                transport=transport.name,
                                transport_price=transport.price,
                                comment=comment,
                                user=user)
    # 链接redis,准备key
    r = get_redis_connection()
    cart_key = f'cart_{user_id}'
    # 准备订单金额
    order_price = 0
    for sku_id in sku_ids:
        # 判断商品是否存在
        try:
            sku = GoodsSKUModel.objects.get(pk=sku_id, is_del=False, is_sale=True)
        except GoodsSKUModel.DoesNotExist:
            return JsonResponse(json_msg(4, '商品不存在'))
        # 获取购物车数量,并作判断
        try:
            count = r.hget(cart_key, sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(5, '商品数量不存在！'))
        # 判断库存
        if sku.stock < count:
            return JsonResponse(json_msg(6, '库存不足!'))
        # 数据合法保存订单详情
        order_goods = OrderGoods.objects.create(order=order,
                                                goods_sku=sku,
                                                price=sku.price,
                                                count=count)
        # 计算订单金额
        order_price += sku.price * count
        # 扣除库存，增加销量
        sku.stock -= count
        sku.sales += count
        sku.save()
    # 支付金额
    pay_money = order_price + transport.price
    # 添加订单金额和支付金额
    order.order_price = order_price
    order.pay_money = pay_money
    order.save()
    # 清空购物车数据
    r.hdel(cart_key, *sku_ids)
    # 合成响应返回
    return JsonResponse(json_msg(0, '购买成功!', data=number))


"""确认支付"""
@check_session
def turepay(request):
    #获取数据
    user_id=request.session.get('id')
    user=UserInfo.objects.get(pk=user_id)
    order=user.oder_set.filter().order_by('-pk').first()
    order_goods=OrderGoods.objects.filter(order=order.pk)
    context={'order':order,'order_goods':order_goods}
    return render(request,'orders/order.html',context=context)

"""支付"""
class Pay(BaseView):

    def get(self,request):
        number=request.GET.get('number')
        order=Oder.objects.get(number=number)
        payments=Payment.objects.all()
        context={'order':order,'payments':payments}
        return render(request,'orders/pay.html',context=context)

    def post(self,request):

        return HttpResponse('OK')
