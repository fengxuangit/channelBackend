#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django import forms
from pages.models import Channel
from utils.tools import encrypt_text
from utils.macro import USER_ROLE

from models import Users

class UserForm(forms.ModelForm):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密 码', widget=forms.PasswordInput)
    confirm_password=forms.CharField(label='重复密码', widget=forms.PasswordInput)
    email = forms.EmailField(label='邮 件')
    role = forms.NumberInput()

    class Meta:
        model = Users
        fields = [
            'username',
            'password',
            'confirm_password',
            'email',
            'role',
        ]
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        cleaned_data["password"] = encrypt_text(password, cleaned_data["username"])

        return self.cleaned_data
