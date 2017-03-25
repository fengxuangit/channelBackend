from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from models import Users
from forms import UserForm
from pages.models import Channel
from utils.models import get_object_or_none


def login(request):
    if request.method == 'POST':
        user = get_object_or_none(Users, username=request)
    return render(request, 'login.html', locals())


def addUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.channel = Channel.objects.create()
            instance.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(reverse('pages:showchannel'))
        else:
            return render(request, 'user.html', {'form': form})
    form = UserForm()
    return render(request, 'user.html', {'form': form})