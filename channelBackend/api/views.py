from django.shortcuts import render

from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
# Create your views here.
from django.db.models import F
from django.db import transaction

from pages.models import Channel
from users.models import OrderInfo

from .serializer import ChannelSerializer, OrderSerializer


class AccountInstall(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin):

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        message = {"code": 200, "status": "success", "data": 0}
        try:
            channel_id = int(request.data['channel'])
            Channel.objects.filter(id=channel_id).update(installnum=F('installnum')+1)
            message['data'] = channel_id
        except Exception,e:
            message = {"code": 100, "status": "Failed", "data": None}

        return Response(message)

class OrderInstall(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin):

    queryset = OrderInfo.objects.all()
    serializer_class = OrderSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def order_create(self, request):
        channel_id = int(request.data['channel'])
        channel = Channel.objects.get(id=channel_id)
        OrderInfo.objects.create(channel=channel, money=int(request.data['money']))
        Channel.objects.update(money=F('money') + int(request.data['money']))
        return True, int(request.data['money'])

    def create(self, request, *args, **kwargs):
        message = {"code": 200, "status": "success", "data": 0}
        try:
            bret, mess = self.order_create(request)
            if not bret:
                raise ValueError("error")
        except Exception,e:
            message = {"code": 100, "status": "Failed", "data": None}

        return Response(message)