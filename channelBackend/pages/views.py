
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings



from users.models import Users, OrderInfo

def index(request):
    return render_to_response('index.html')


def showchannel(request):
    user_list = Users.objects.all()
    paginator = Paginator(user_list, settings.ONE_PAGE_NUM)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render_to_response('details.html', {'users': users})


def orderinfo(request):
    order_list = OrderInfo.objects.all()
    paginator = Paginator(order_list, settings.ONE_PAGE_NUM)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render_to_response('orders.html', {'orders': orders})