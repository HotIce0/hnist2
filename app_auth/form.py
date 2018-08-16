from django import forms
import re

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from app_db import models

# 注册表单
from app_auth import student_auth


# 验证成功，测返回用户的认证信息
class RegisterForm(forms.Form):
    def is_valid(self):
        if super().is_valid():
            is_valid = True
            # 验证身份证字段
            if re.match(r'^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X)$', self.data.get('id_card')) is None:
                self.add_error('id_card', '身份证号码格式有误')
                is_valid = False

            # 验证密码是否一致
            if not self.data.get('password') == self.data.get('re_password'):
                self.add_error('re_password', '两次输入的密码不一致')
                is_valid = False

            # 验证学生信息是否一致。姓名，身份证号码，学号
            auth_res = student_auth.auth(self.data.get('real_name'), self.data.get('id_card'), self.data.get('stu_id'))
            if not auth_res:
                self.add_error('id_card', '学生信息不一致')
                is_valid = False

            # 验证用户名是否已经存在
            try:
                models.User.objects.get(name=self.data.get('user_name'))
                self.add_error('user_name', '该用户名已存在')
                is_valid = False
            except ObjectDoesNotExist:
                pass

            # 验证身份证是否已经存在
            try:
                models.User.objects.get(card_id=self.data.get('id_card'))
                self.add_error('id_card', '该身份证已被注册')
                is_valid = False
            except ObjectDoesNotExist:
                pass

            # # 验证邮箱是否已存在
            # try:
            #     models.User.objects.get(email=self.data.get('email'))
            # except ObjectDoesNotExist:
            #     self.add_error('email', '该邮箱已存在')
            #     is_valid = False

        return auth_res if is_valid else is_valid

    # 用户名（昵称）
    user_name = forms.CharField(required=True,
                                max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                                )
    # 邮箱
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                             )
    # 密码
    password = forms.CharField(required=True,
                               max_length=16,
                               widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                               )
    # 再次输入密码
    re_password = forms.CharField(required=True,
                                  max_length=16,
                                  min_length=6,
                                  widget=forms.PasswordInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                                  )
    # 真实姓名
    real_name = forms.CharField(required=True,
                                max_length=11,
                                widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '必填'}))

    # 学号
    stu_id = forms.CharField(required=True,
                             max_length=11,
                             min_length=11,
                             widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                             )
    # 身份证
    id_card = forms.CharField(required=True,
                              max_length=18,
                              widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': '必填'})
                              )
