#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'

from django.conf.urls import url

from views import AccountInstall, OrderInstall

urlpatterns = [
    # url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^install$', AccountInstall.as_view({'get': 'list', 'post': 'create'}), name='install'),
    url(r'^order', OrderInstall.as_view({'get': 'list', 'post': 'create'}), name='order'),
]
