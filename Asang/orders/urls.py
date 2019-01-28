from django.conf.urls import url

from orders.views import order

urlpatterns = [
        url('^order/$',order,name='订单')
]