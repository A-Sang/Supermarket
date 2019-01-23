from django.conf.urls import url

from goods.views import IndexView, DetailView, ListView, CateGoryView

urlpatterns=[
        url('^index/$',IndexView.as_view(),name='超市主页'),
        url('^detail/$',DetailView.as_view(),name='商品详情'),
        url('^list/$',ListView.as_view(),name='商品列表'),
        url('^category/$',CateGoryView.as_view(),name='商品分类'),
]