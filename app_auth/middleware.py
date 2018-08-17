from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.utils.functional import SimpleLazyObject

from app_auth.auth_settings import AUTH_SETTINGS
from app_db import models


def get_user(request):
    # 获取用户实例，如果获取不到就返回False
    try:
        return models.User.objects.get(id=request.session.get('user2_id'))
    except ObjectDoesNotExist:
        return False


def is_login(request):
    try:
        request.session['user2_id']
        return True
    except KeyError:
        return False


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 主页取消登陆要求
        if request.path == AUTH_SETTINGS.get('home_url'):
            pass
        # 过滤登陆和注册请求
        elif request.path == AUTH_SETTINGS.get('login_url') or request.path == AUTH_SETTINGS.get('register_url'):
            if is_login(request):
                return HttpResponseRedirect(AUTH_SETTINGS.get('home_url'))
            pass
        else:
            # 登陆状态判断
            if not is_login(request):
                return HttpResponseRedirect(AUTH_SETTINGS.get('login_url'))
            # 添加user2（用户实例）到request
            request.user2 = SimpleLazyObject(lambda: get_user(request))

        response = self.get_response(request)
        return response
