import re

from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from .form import RegisterForm
# Create your views here.
from app_db import models


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'app_auth/register.html', {
            'form': form
        })
    else:
        form = RegisterForm(request.POST)
        # 注册表单验证 (包括身份证，以及密码是否一致，以及学生学号与身份证是否一致)
        auth_res = form.is_valid()
        if auth_res:
            # print(form.non_field_errors())
            # 验证通过，新增用户，默认角色为普通用户
            user = models.User()
            form.cleaned_data.get('')


            return HttpResponse('验证正确')
    # 验证未通过
    return render(request, 'app_auth/register.html', {
        'form': form
    })


def login(request):
    return HttpResponse('login')