from django.conf.urls import url
from user.views import LoginView, RegisterView, NewPwdView, ForPwdView, BoundPhoneView, saftystep, PaymentView, member, \
    GiAddressView, EditAddressView, AddressView, InfoView, delete, SendMsm

urlpatterns = [
    url('^login/$', LoginView.as_view(), name='登录'),
    url('^reg/$', RegisterView.as_view(), name='注册'),
    url('^newpwd/$', NewPwdView.as_view(), name='修改登录密码'),
    url('^forpwd/$', ForPwdView.as_view(), name='忘记密码'),
    url('^newphone/$', BoundPhoneView.as_view(), name='绑定新手机号'),
    url('^safty/$', saftystep, name='安全设置'),
    url('^payment/$', PaymentView.as_view(), name='支付密码'),
    url('^giaddress/$', GiAddressView.as_view(), name='地址管理'),
    url('^editaddress/$', EditAddressView.as_view(), name='编辑地址'),
    url('^address/$', AddressView.as_view(), name='添加地址'),
    url('^info/$', InfoView.as_view(), name='个人信息'),
    url('^member/$', member, name='个人中心'),
    url('^del/$', delete, name='删除地址'),
    url('^sendmsg/$', SendMsm.as_view(), name='发送验证码'),
]
