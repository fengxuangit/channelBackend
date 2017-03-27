#-*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from  utils.macro import USER_ROLE

from pages.models import Channel

# class UserManager(BaseUserManager):
#     def create_user(self, name, email, password=None):
#         if not email:
#             raise ValueError("user must have a email address")
#         user = self.model(name=name, email=UserManager.normalize_email(email))
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, name, email, password=None):
#         user = self.create_user(name, email, password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser):
#     '''
#     用户表
#     '''
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=40)
#     channel = models.ForeignKey(Channel, related_name='User')
#     email = models.EmailField(unique=True)
#     role = models.IntegerField(default=2)
#     last_login_time = models.DateTimeField(null=True)
#     last_ip = models.CharField(max_length=20, null=True)
#     avatar = models.URLField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     access_token = models.CharField(max_length=100, blank=True)
#     refresh_token = models.CharField(max_length=100, blank=True)
#     expires_in = models.BigIntegerField(max_length=100, default=0)
#
#     objects = UserManager
#
#     USERNAME_FIELD = 'username'
#
#     REQUIRED_FIELDS = ['email',]
#
#     ordering = ('-created_at')
#
#     def is_staff(self):
#         return self.is_admin
#
#     def get_full_name(self):
#         return "{0}_{1}".format(self.username, self.email)
#
#     def get_short_name(self):
#         return self.username


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=40)
    channel = models.ForeignKey(Channel, related_name='User')
    email = models.EmailField(unique=True)
    role = models.IntegerField(default=USER_ROLE.OWNER)
    last_login_time = models.DateTimeField(null=True)
    last_ip = models.CharField(max_length=20, null=True)

    def update_login_info(self, request):
        self.last_login_time = datetime.datetime.now()
        self.last_ip = request.META['REMOTE_ADDR']
        self.save(update_fields=['last_login_time', 'last_ip'])

    def is_admin_or_manager(self):
        if self.role == USER_ROLE.MANAGER:
            return True
        return False

    is_admin = property(is_admin_or_manager)

class OrderInfo(models.Model):
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, related_name='OrderInfo')
    money = models.IntegerField()
    insert_tm = models.DateTimeField(auto_now_add=True)