#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django.contrib.auth.middleware import SessionAuthenticationMiddleware

from users.models import Users
from .models import get_object_or_none

class ChannelSessionAuthentication(SessionAuthenticationMiddleware):
    '''
    channelBackend session authenticate
    '''

    def process_request(self, request):
        session = getattr(request, 'session', {})
        if session.has_key('username'):
            username = session.get('username')
            user = get_object_or_none(Users, username=username)
            request.__setattr__('user', user)