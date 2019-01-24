from django.conf.urls import url

from goods.views import IndexView, DetailView, CateGoryView

urlpatterns=[
        url('^index/$',IndexView.as_view(),name='超市主页'),
        url('^detail/(?P<id>\d+)$',DetailView.as_view(),name='商品详情'),
        url('^category/(?P<id>\d+)$',CateGoryView.as_view(),name='商品分类'),
]