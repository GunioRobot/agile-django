from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       PasswordChangeForm)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.db import transaction

from agile.forms import *
from agile.models import *
from agile.decorators import *

# Create your views here.

def index(request):
    return render_to_response('index.html', RequestContext(request))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('agile_index'))
    form = AuthenticationForm()
    
    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(request.GET.get('next', reverse('agile_index')))
        
    return render_to_response('login.html', RequestContext(request, {
        'form': form,
    }))
    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('agile_index'))

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('agile_index'))
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('agile_index'))
        
    return render_to_response('signup.html', RequestContext(request, {
        'form': form,
    }))

@login_required
def profile(request):
    user_form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    
    form_saved = None
    
    if request.method == 'POST':
        
        if request.POST.get('form') == 'user':
            user_form = UserProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                form_saved = 'user'
        
        elif request.POST.get('form') == 'pass':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                password_form = PasswordChangeForm(request.user)
                form_saved = 'password'
    
    return render_to_response('profile/profile.html', RequestContext(request, {
        'password_form': password_form,
        'user_form': user_form,
        'form_saved': form_saved
    }))

@login_required
def projects(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('agile_projects'))
    
    return render_to_response('project/add.html', RequestContext(request, {
        'form': form,
    }))
    
@login_required
def project(request, project_id):
    project = get_object_or_404(request.user.projects, id=project_id)
    story_form = StoryForm()
    users = project.users
    story_form.fields['creator'].queryset = users
    story_form.fields['owner'].queryset = users
    return render_to_response('project/board.html', RequestContext(request, {
        'project': project,
        'story_form': story_form,
    }))
    
@login_required
@render_to_json
def story(request, project_id, story_number, action):
    
    if not (request.method == 'POST' and request.is_ajax()):
        return {
            'success': False
        }
        
    story = Story.objects.get(phase__project=project_id, number=story_number)
    
    if action == 'move':
        new_index = int(request.POST.get('index'))
        new_phase_id = int(request.POST.get('phase'))
        story.move(new_phase_id=new_phase_id, new_index=new_index)
        
    elif action == 'edit':
        story.name = request.POST.get('name')
        story.save()


@login_required
@render_to_json
def story_add(request, project_id):
    
    if not (request.method == 'POST' and request.is_ajax()):
        return {
            'success': False
        }
    
    story_form = StoryForm(request.POST)
    if story_form.is_valid():
        
        project = Project.objects.get(id=project_id)
        phase = project.phases.all().order_by('index')[0]
        
        story = story_form.save(commit=False)
        story.phase = phase
        story.save()
        return
    
    else:
        return {
            'success': False,
            'error': [
                {unicode(story_form.fields[field].label): error}
            for field, error in story_form.errors.iteritems()], 
        }
        
    return {
        'success': False
    }

