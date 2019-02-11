# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseView
from db.helper import json_msg, get_count, check_session, get_price
from goods.models import GoodsSKUModel


class CartView(BaseView):

    def get(self, request):
        # 获取参数
        user_id = request.session.get('id')
        # 拼接key
        cart_key = f"cart_{user_id}"
        # 操作数据库
        r = get_redis_connection()
        # 字典推导式遍历数据，返回sku对象和数量
        goods = {GoodsSKUModel.objects.get(pk=int(pk)): int(counts) for pk, counts in r.hgetall(cart_key).items()}
        # 推导式获取各个商品总价价格，返回列表
        # price_list=[sku.price*count for sku,count in goods.items()]
        # for sku in goods.keys():
        #     price_list.append(sku.price)
        # 计算总价格
        # total_price=0
        # for price in price_list:
        #     total_price += price
        context = {
            'goods': goods,

        }
        return render(request, 'shopcart/shopcart.html', context=context)

    def post(self, request):
        # 接收参数
        user_id = request.session.get('id')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 验证参数是否合法
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, '参数错误'))
        # 参数正确，操作数据库
        r = get_redis_connection()
        # 设置redis的key
        cart_key = f'cart_{user_id}'
        # 判断商品是否存在（下架）
        try:
            sku = GoodsSKUModel.objects.get(pk=sku_id, is_del=False, is_sale=True)
        except GoodsSKUModel.DoesNotExist:
            # 删除购物车信息
            r.hdel(cart_key, sku_id)
            return JsonResponse(json_msg(2, '该商品已下架'))
        # 判断商品库存是否充足
        if sku.stock < count:
            return JsonResponse(json_msg(3, '商品库存不足'))

        # 判断购物里的数量和现添加的数量是否大于库存
        old_count = r.hget(cart_key, sku_id)
        if old_count is None:
            # redis没有值返回None
            old_count = 0
        else:
            # 数据为二进制，要转码
            old_count = int(old_count)

        if sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))
        # incerby给值增量
        r.hincrby(cart_key, sku_id, count)
        # 获取购物车总数量
        count_cart = get_count(request)
        return JsonResponse(json_msg(0, '添加成功', count_cart))


@check_session
def add_cart(request):
    # 接收参数
    user_id = request.session.get('id')
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    # 验证参数是否合法
    try:
        sku_id = int(sku_id)
        count = int(count)
    except:
        return JsonResponse(json_msg(1, '参数错误'))
    # 判断商品是否存在（下架）
    try:
        sku = GoodsSKUModel.objects.get(pk=sku_id, is_del=False)
    except GoodsSKUModel.DoesNotExist:
        return JsonResponse(json_msg(2, '该商品已下架'))
    # 判断商品库存是否充足
    if sku.stock < count:
        return JsonResponse(json_msg(3, '商品库存不足'))
    # 参数正确，操作数据库
    r = get_redis_connection()
    # 设置redis的key
    cart_key = f'cart_{user_id}'
    # 判断购物里的数量和现添加的数量是否大于库存
    old_count = r.hget(cart_key, sku_id)
    if old_count is None:
        # redis没有值返回None
        old_count = 0
    else:
        # 数据为二进制，要转码
        old_count = int(old_count)
    if sku.stock < old_count + count:
        return JsonResponse(json_msg(3, "库存不足!"))
    # incerby给值增量
    r.hincrby(cart_key, sku_id, count)
    # 获取购物车总数量
    count_cart = get_count(request)
    # 获取总金额
    total_price = get_price(request)
    data = {'count_cart': count_cart,
            'total_price': total_price}
    return JsonResponse(json_msg(0, '添加成功', data))


@check_session
def minus_cart(request):
    # 接收参数
    user_id = request.session.get('id')
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    # 拼接key
    cart_id = f"cart_{user_id}"
    # 检查数据
    try:
        sku_id = int(sku_id)
        count = int(count)
    except:
        return JsonResponse(json_msg(1, '参数错误'))
    # 操作数据库
    r = get_redis_connection()
    r.hincrby(cart_id, sku_id, count)
    # 获取购物车总数量
    count_cart = get_count(request)
    # 获取总金额
    total_price = get_price(request)
    data = {'count_cart': count_cart,
            'total_price': total_price}
    # 合成响应返回
    return JsonResponse(json_msg(0, '减少成功', data))


@check_session
def del_cart(request):
    # 接收参数
    user_id = request.session.get('id')
    sku_id = request.POST.get('sku_id')
    # 拼接key
    cart_key = f"cart_{user_id}"
    # 检查数据
    try:
        sku_id = int(sku_id)
    except:
        return JsonResponse(json_msg(1, '参数错误'))
    # 操作数据库
    r = get_redis_connection()
    r.hdel(cart_key, sku_id)
    goods = {GoodsSKUModel.objects.get(pk=int(pk)): int(counts) for pk, counts in r.hgetall(cart_key).items()}
    data = {'goods': goods}
    # 合成响应返回
    return JsonResponse(json_msg(0, '删除成功'))
