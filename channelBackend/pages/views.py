
from django.shortcuts import render_to_response, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from utils.tools import channel_login_required

from pages.models import Channel
from users.models import Users, OrderInfo

@channel_login_required
def index(request):
    return render_to_response('index.html')


@channel_login_required
def orderinfo(request):
    # import ipdb;ipdb.set_trace()
    if request.user.is_admin:
        order_list = OrderInfo.objects.all()
    else:
        order_list = OrderInfo.objects.filter(channel=request.user.channel)
    paginator = Paginator(order_list, settings.ONE_PAGE_NUM)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render(request, 'orders.html', locals())


@channel_login_required
def showusers(request):
    if request.user.is_admin:
        user_list = Users.objects.all()
    else:
        user_list = Users.objects.filter(id=request.user.id)
    paginator = Paginator(user_list, settings.ONE_PAGE_NUM)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'details.html', locals())

