#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django import forms
from pages.models import Channel

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

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        return self.cleaned_data
