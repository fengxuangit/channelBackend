#!/usr/bin/env python
# -*- coding: utf-8 -*- # 
__author__ = 'fengxuan'
import hashlib

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