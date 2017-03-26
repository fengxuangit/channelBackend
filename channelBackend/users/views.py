from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from models import Users
from forms import UserForm
from pages.models import Channel
from utils.models import get_object_or_none
from utils.tools import check_encrypted_text, channel_login_required


def login(request):
    if request.method == 'POST':
        user = get_object_or_none(Users, username=request.POST.get('username', None))
        if not user or not check_encrypted_text(request.POST.get('password', None),
                                    user.username, user.password):
            return render(request, 'login.html', {'errors': 'username or password not valid!'})
        request.__setattr__('user', user)
        request.session['username'] = user.username
        return HttpResponseRedirect(reverse('pages:orderinfo'))
    return render(request, 'login.html', locals())


def logout(request):
    request.session['username'] = ''
    del request.session['username']
    request.session.delete()
    return HttpResponseRedirect(reverse('login'))


@channel_login_required
@transaction.atomic()
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None, user=request.session.get('username', None))
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


