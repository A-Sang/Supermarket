from django.conf.urls import url

from shopcart.views import CartView, add_cart, minus_cart, del_cart

urlpatterns = [
    url('^cart/$', CartView.as_view(), name='购物车'),
    url('^add/$', add_cart, name='增加'),
    url('^minus/$', minus_cart, name='减少'),
    url('^del/$', del_cart, name='删除'),
]