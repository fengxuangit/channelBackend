#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django.conf.urls import include, url

from views import (
    index,
    showchannel,
    orderinfo,
    )

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^pages/showchannel', showchannel, name='showchannel'),
    url(r'^pages/orderinfo', orderinfo, name='orderinfo'),
]