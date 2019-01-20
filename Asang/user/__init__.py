import hashlib

from django.shortcuts import redirect

from Asang.settings import SECRET_KEY


def hash_password(password):
    # 哈希,加盐
    for _ in range(3000):
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.sha256(pass_str.encode('utf-8'))
        password = h.hexdigest()
        return password


def set_session(request, user):
    #设置session,验证没有id则返回登录页面
    request.session['id'] = user.pk
    request.session['phone_num']=user.phone_num
    request.session['is_login'] = 'YES'
    #设置session过期时间,不填为两周,0为关闭浏览器过期,固定过期时间,None永不过期
    request.session.set_expiry(None)


def check_session(func):
    def new (request,*args,**kwargs):
        if request.session.get('id') is None:
            return redirect('user:登录')
        else:
            #如果有session调用原函数
            return func(request,*args,**kwargs)
    #返回新函数
    return new
