from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from models import Users
from forms import UserForm
from pages.models import Channel
from utils.models import get_object_or_none
from utils.tools import check_encrypted_text


@transaction.atomic()
def login(request):
    if request.method == 'POST':
        user = get_object_or_none(Users, username=request.POST.get('username', None))
        if not user or not check_encrypted_text(request.POST.get('password', None),
                                    user.username, user.password):
            return render(request, 'login.html', {'errors': 'username or password not valid!'})
        import ipdb;ipdb.set_trace()
        return HttpResponseRedirect(reverse('pages:orderinfo'))
    return render(request, 'login.html', locals())


@transaction.atomic()
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.channel = Channel.objects.create()
            instance.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(reverse('users:showchannel'))
        else:
            return render(request, 'user.html', {'form': form})
    form = UserForm()
    return render(request, 'user.html', {'form': form})


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

