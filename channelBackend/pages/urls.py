#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django.conf.urls import include, url

from views import (
    index,
    orderinfo,
    )

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^pages/orderinfo', orderinfo, name='orderinfo'),
]