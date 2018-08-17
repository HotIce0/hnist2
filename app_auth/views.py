import re

from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app_auth.email_active_token import Token
from .form import RegisterForm, LoginForm, ActiveEmailSendForm
from app_db import models

# Create your views here.


# 注册的路由
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
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            return render(request, 'app_auth/register.html', {
                'form': form
            })


# 登陆的路由
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'app_auth/login.html', {
            'form': form
        })
    else:
        form = LoginForm(request.POST)
        # 登陆表单验证
        if form.is_valid():
            # 保存用户登陆状态到session
            user = models.User.objects.get(student_id=form.cleaned_data.get('stu_id'))
            user.login(request)
            # 判断账号是否激活
            if user.is_active:
                return HttpResponse('已经激活')
            else:
                # 未激活，跳转到激活页面。
                return HttpResponseRedirect(reverse('auth:active'))
        else:
            return render(request, 'app_auth/login.html', {
                'form': form
            })


# 注销登陆的路由
def logout(request):
    # print(request.user2.real_name)
    request.user2.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


# 发送激活邮件的路由
def active(request):
    if request.user2.is_active:
        return HttpResponseRedirect(reverse('shop:index'))
    if request.method == 'GET':
        form = ActiveEmailSendForm(initial={'email': request.user2.email})
        return render(request, 'app_auth/active.html', {
            'form': form
        })
    else:
        form = ActiveEmailSendForm(request.POST)
        if form.is_valid():
            token = Token()
            # 生成邮箱激活url
            active_token_url = request.get_host() + \
                           reverse('auth:active_email',
                                   args=[token.generate_email_active_token(request.user2.student_id)]  # 生成邮件激活链接的token
                                   )

            if send_mail(subject='账号激活',
                         message='',
                         html_message=render(request, 'app_auth/active_email.html', {
                             'url': active_token_url,
                             'username': request.user2.real_name
                         }).content.decode(encoding='utf-8'),
                         recipient_list=[form.cleaned_data.get('email')],
                         fail_silently=True,
                         from_email=None) > 0:
                form.add_error(None, '发送成功！')
            else:
                form.add_error(None, '邮件发送失败！')

        return render(request, 'app_auth/active.html', {
            'form': form
        })


# 验证激活url的路由
def active_email(request, token):
    # 判断是否已经激活
    if request.user2.is_active:
        return HttpResponseRedirect(reverse('shop:index'))
    # token验证类
    token_obj = Token()
    user = request.user2
    # 验证是否一致，以及url是否过期
    if user.student_id == token_obj.confirm_email_active_token(token):
        user.is_active = True
        user.save()
        # 激活成功
        return HttpResponse('激活成功')
    else:
        return HttpResponse('激活url已经过期，请重新获取激活邮件')
