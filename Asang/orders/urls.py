from django.conf.urls import url

from orders.views import orderlist, tureorder, save_order, turepay, Pay

urlpatterns = [
        url('^order/$',orderlist,name='订单'),
        url('^tureorder/$',tureorder,name='确认订单'),
        url('^save_order/$',save_order,name='保存订单'),
        url('^turepay/$',turepay,name='确认支付'),
        url('^pay/$',Pay.as_view(),name='支付'),
]