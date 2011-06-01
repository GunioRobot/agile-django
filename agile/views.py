from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       PasswordChangeForm)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.db import transaction
from django.views.decorators.cache import never_cache

from gravatar.templatetags.gravatar import gravatar

from agile.forms import *
from agile.models import *
from agile.decorators import *

################################################################################
# Views
################################################################################

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
    userprofile = request.user.agile_userprofile
    user_form = UserDataForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    settings_form = UserProfileForm(instance=userprofile)
    
    form_saved = None
    
    if request.method == 'POST':
        
        if request.POST.get('form') == 'user':
            user_form = UserDataForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                form_saved = 'user'
        
        elif request.POST.get('form') == 'password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                password_form = PasswordChangeForm(request.user)
                form_saved = 'password'
        
        elif request.POST.get('form') == 'settings':
            settings_form = UserProfileForm(request.POST, instance=userprofile)
            if settings_form.is_valid():
                settings_form.save()
                form_saved = 'settings'
    
    return render_to_response('agile/profile/profile.html', RequestContext(request, {
        'password_form': password_form,
        'user_form': user_form,
        'settings_form': settings_form,
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
    
    return render_to_response('agile/project/add.html', RequestContext(request, {
        'form': form,
    }))
    
@login_required
def project(request, project_id):
    project = request.user.projects.get(pk=project_id)
    initial = {
        'creator': request.user,
    }
    story_form = StoryForm(initial=initial, project=project)
    
    return render_to_response('agile/project/board.html', RequestContext(request, {
        'project': project,
        'story_form': story_form,
    }))
    
@login_required
def project_details(request, project_id):
    project = request.user.projects.get(pk=project_id)
    project_form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return HttpResponseRedirect(project.get_details_url())
    
    return render_to_response('agile/project/details.html', RequestContext(request, {
        'project': project,
        'project_form': project_form,
    }))
    
@login_required
def phase(request, project_id):
    project = request.user.projects.get(pk=project_id)
    phase_form = PhaseForm()
    return render_to_response('agile/phase/process.html', RequestContext(request, {
        'project': project,
        'phase_form': phase_form,
    }))
    
@login_required
@render_to_json
def phase_ajax(request, project_id, phase_id, action=None):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
    
    if action == 'move':
        project = request.user.projects.get(pk=project_id)
        phase = project.phases.get(id=phase_id)
        phase.move(request.POST.get('index'))
    
@login_required
def story(request, project_id, story_number):
    
    project = request.user.projects.get(pk=project_id)
    story = project.stories.get(number=story_number)
    
    comment_form = CommentForm()
    task_form = TaskForm(project=project)
    story_form = StoryForm(instance=story, project=project)
    
    return render_to_response('agile/story/details.html', RequestContext(request, {
        'project': project,
        'story': story,
        'story_form': story_form,
        'comment_form': comment_form,
        'task_form': task_form,
    }))


@login_required
@render_to_json
def story_ajax(request, project_id, story_number, action=None):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
    
    project = request.user.projects.get(pk=project_id)
    story = project.stories.get(number=story_number)
    
    if action == 'move':
        new_index = request.POST.get('index')
        new_index = int(new_index) if new_index else None
        new_phase_id = int(request.POST.get('phase', -1))
        story.move(new_phase_id=new_phase_id, new_index=new_index)
        
    elif action == 'edit':
        story_form = StoryForm(project=project)
        def change_value(key):
            value = request.POST.get(key)
            value = story_form.fields[key].clean(value)
            setattr(story, key, value)
            story.save()
        
        if request.POST.has_key('name'):
            change_value('name')
            
        if request.POST.has_key('description'):
            change_value('description')
            return {
                'html': render_to_string('agile/story/description.html', {
                    'story': story,
                }, RequestContext(request)),
            }
        
        if request.POST.has_key('owner') or request.POST.has_key('creator'):
            if request.POST.has_key('owner'):
                key = 'owner'
            elif request.POST.has_key('creator'):
                key = 'creator'
            change_value(key)
            user = getattr(story, key)
            return {
                'html': gravatar(user, size=30) if user else '',
            }
        
    elif action == 'comment':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.story = story
            comment.save()
            return {
                'html': render_to_string('agile/story/comment.html', {
                    'comment': comment,
                }, RequestContext(request)),
            }
            
        else:
            errors = {}
            for field, error in comment_form.errors.iteritems():
                errors[unicode(comment_form.fields[field].label)] = error 
        
            return {
                'success': False,
                'error': errors, 
            }
    
    elif action == 'delete':
        story.delete()
        


@login_required
@render_to_json
def story_add(request, project_id):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
        
    project = request.user.projects.get(pk=project_id)
    story_form = StoryForm(project, request.POST)
    if story_form.is_valid():
        story = story_form.save(commit=False)
        story.save()
        return {
            'html': render_to_string('agile/project/story.html', {
                'story': story,
            }, RequestContext(request)),
            'phase_index': story.phase.index,
        }
    
    else:
        errors = {}
        for field, error in story_form.errors.iteritems():
            errors[unicode(story_form.fields[field].label)] = error 
        
        return {
            'success': False,
            'error': errors, 
        }
        
    return {
        'success': False
    }

@login_required
@render_to_json
def comment(request, project_id, story_number, comment_id, action=None):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
    
    comment = request.user.comments.get(pk=comment_id)
    if action == 'delete':
        comment.delete()
        
@login_required
@render_to_json
def tag(request, project_id, story_number, tag_id, action=None):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
    
    project = request.user.projects.get(pk=project_id)
    tag = project.stories.get(number=story_number).tags.get(pk=tag_id)
    
    if action == 'delete':
        tag.delete()
