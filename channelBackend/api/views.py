from django.shortcuts import render

from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
# Create your views here.

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
            channel_id = int(request.data['channel_id'])
            channel = Channel.objects.get(id=channel_id)
            Channel.objects.filter(id=channel_id).update(installnum=(channel.installnum +1))
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


    def create(self, request, *args, **kwargs):
        message = {"code": 200, "status": "success", "data": 0}
        try:
            channel_id = int(request.data['channel_id'])
            channel = Channel.objects.get(id=channel_id)
            order = OrderInfo.objects.create(channel=channel, money=int(request.data['money']))
            Channel.objects.update(money=int(request.data['money']))
            message['data'] = int(request.data['money'])
        except Exception,e:
            message = {"code": 100, "status": "Failed", "data": None}

        return Response(message)