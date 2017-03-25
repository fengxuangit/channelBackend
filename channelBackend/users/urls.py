#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django.conf.urls import include, url

from views import (
    addUser,
    login,
    )

urlpatterns = [
    url(r'^login', login, name='login'),
    url(r'^adduser', addUser, name='adduser'),
]