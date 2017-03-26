#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
from django.core.exceptions import PermissionDenied
from django.contrib.auth.middleware import SessionAuthenticationMiddleware

from users.models import Users
from .models import get_object_or_none

class ChannelSessionAuthentication(SessionAuthenticationMiddleware):
    '''
    channelBackend session authenticate
    '''

    def process_request(self, request):
        request = request._request
        session = getattr(request, 'session', {})
        if not session.has_key('username'):
            session['username'] = ''
            raise PermissionDenied(u"认证失败")

        username = session.get('username')
        if not username:
            raise PermissionDenied(u"认证失败")
        try:
            user = get_object_or_none(Users, username=username)
            return user, None
        except Users.DoesNotExist:
            raise PermissionDenied(u'认证失败')

        request.__setattr__('user', user)
