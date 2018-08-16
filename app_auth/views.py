import re

from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.http import HttpResponse
from django.shortcuts import render
from .form import RegisterForm
from app_db import models
# Create your views here.


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
            user.name = form.cleaned_data.get('user_name')
            user.avatar = '默认头像url'
            user.real_name = form.cleaned_data.get('real_name')
            user.student_id = form.cleaned_data.get('stu_id')
            user.card_id = form.cleaned_data.get('id_card')
            user.sex = 0 if auth_res.get('is_man') else 1  # 0是男生，1是女生
            user.email = form.cleaned_data.get('email')
            user.password = make_password(form.cleaned_data.get('password'))
            # 存储用户数据到数据库
            user.save()
            # 跳转到登陆页面
            return HttpResponse('注册成功!')
    # 验证未通过
    return render(request, 'app_auth/register.html', {
        'form': form
    })


def login(request):
    return HttpResponse('login')
