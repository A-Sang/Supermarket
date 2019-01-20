from django.utils.decorators import method_decorator
from django.views import View

from user import check_session


class BaseView(View):
#自定义视图基类,当需要验证session才显示页面时继承
    @method_decorator(check_session)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)