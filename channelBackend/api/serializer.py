#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'

from rest_framework.serializers import Serializer

from pages.models import Channel
from users.models import OrderInfo

class ChannelSerializer(Serializer):

    class Meta:
        models = Channel
        fields = ['id', 'installnum', 'money', 'charge', 'update_tm']

class OrderSerializer(Serializer):

    class Meta:
        models = OrderInfo
        fields = ['id', 'channel', 'money', 'insert_tm']