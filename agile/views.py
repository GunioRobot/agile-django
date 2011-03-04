from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext

from agile.forms import *

# Create your views here.

def index(request):
    return render_to_response('index.html', RequestContext(request))

def login(request):
    form = AuthenticationForm()
    message = False
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('agile_index'))
        else:
            message = True
        
    return render_to_response('login.html', RequestContext(request, {
        'form': form,
        'error': message,
    }))
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('agile_index'))

@login_required
def projects(request):
    form = ProjectForm()
    message = False
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            message = False
        else:
            error = True
            
    return render_to_response('project/add.html', RequestContext(request, {
        'form': form,
        'error': message,
    }))
