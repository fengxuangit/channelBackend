
from django.shortcuts import render_to_response, render
from django.db import connection
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
    cursor = connection.cursor()
    order_list = []
    if request.user.is_admin:
        cursor.execute('select `users_orderinfo`.`id`,`users_users`.`username` ,`users_orderinfo`.`channel_id`,'
                       '`users_orderinfo`.`money`,`users_orderinfo`.`insert_tm` from users_orderinfo '
                       'inner join users_users on `users_orderinfo`.channel_id = `users_users`.channel_id;')
        order_list = cursor.fetchall()
    else:
        cursor.execute('select `users_orderinfo`.`id`,`users_users`.`username` ,`users_orderinfo`.`channel_id`,'
                       '`users_orderinfo`.`money`,`users_orderinfo`.`insert_tm` from users_orderinfo '
                       'inner join users_users on `users_orderinfo`.channel_id = `users_users`.channel_id'
                       ' where `users_users`.id = %d' % request.user.id)
        order_list.append(cursor.fetchone())
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

