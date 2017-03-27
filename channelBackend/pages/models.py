from __future__ import unicode_literals

from django.db import models


class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    installnum = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    charge = models.IntegerField(default=0)
    update_tm = models.DateTimeField(auto_now_add=True)