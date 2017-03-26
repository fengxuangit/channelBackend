
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from utils.tools import channel_login_required


from users.models import Users, OrderInfo

@channel_login_required
def index(request):
    return render_to_response('index.html')


@channel_login_required
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


@channel_login_required
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

