#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
import hashlib
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def encrypt_text(text, salt=None):
    try:
        hasher = hashlib.sha1()
        hasher.update(str(text) + str(salt) if salt else '')
        return hasher.hexdigest()
    except Exception, e:
        return None


def check_encrypted_text(text, salt, encoded):
    new_encoded = encrypt_text(text, salt)
    if new_encoded == encoded:
        return True
    else:
        return False


def channel_login_required(func):
    def warp(request, *args, **kwargs):
        if 'username' not in request.session.keys() or not request.session['username']:
            return HttpResponseRedirect(reverse('login'))
        return func(request, *args, **kwargs)
    warp.__doc__ = func.__doc__
    warp.__name__ = func.__name__

    return warp