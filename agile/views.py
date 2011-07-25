import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       PasswordChangeForm)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate
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
                profile = settings_form.save()
                activate(profile.user_language)
                request.session['django_language'] = profile.user_language
                request.LANGUAGE_CODE = profile.user_language
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
@require_POST
def add_phase(request, project_id):
    if not request.is_ajax():
        raise Http404
    project = request.user.projects.get(pk=project_id)
    phase_form = PhaseForm(request.POST)
    if phase_form.is_valid():
        phase = phase_form.save(commit=False)
        phase.index = project.phases.count()
        phase.project = project
        phase.save()
        phase.move(phase.index)
        return {
            'success': True
        }
    else:
        errors = {}
        for field, error in phase_form.errors.iteritems():
            errors[unicode(phase_form.fields[field].label)] = error
        return {
            'success': False,
            'errors': errors
        }

@login_required
@render_to_json
@require_POST
def phase_ajax(request, project_id, phase_id, action=None):
    
    if not request.is_ajax():
        raise Http404
    
    project = request.user.projects.get(pk=project_id)
    phase = project.phases.get(id=phase_id)
    
    if action == 'move':
        phase.move(request.POST.get('index'))
    
    # This retrieves the requested phase data and renders the filled form
    if action == 'get':
        phase_form = PhaseForm(instance=phase)
        return {
            'html': render_to_string('agile/phase/update.html', {
                'project': project,
                'phase': phase,
                'phase_form': phase_form,
            }, RequestContext(request)),
        }
    
    # This processes the posted data and updates the requested Phase object
    if action == 'edit':
        phase_form = PhaseForm(request.POST, instance=phase)
        if phase_form.is_valid():
            phase_form.save()
            return
        errors = {}
        for field, error in phase_form.errors.iteritems():
                errors[unicode(phase_form.fields[field].label)] = error
        return {
            'success': False,
            'errors': errors
        }
    
    if action == 'delete':
        if phase.is_backlog:
            return {
                'success': False,
                'error': 'Cannot delete this phase. '
                    'This phase is Backlog.'
            }
        elif phase.is_archive:
            return {
                'success': False,
                'error': 'Cannot  delete this phase. '
                    'This phase is Archive.'
            }
        elif phase.has_stories:
            return {
                'success': False,
                'error': 'Cannot delete this phase. '
                    'This phase has Stories.'
            }
        phase.delete()
        return

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
        
    elif action == 'time_entry':
        time_entries = TimeEntry.objects.filter(user=request.user, stop_at=None)
        if not time_entries.exists():
            time_entry = TimeEntry()
            time_entry.user = request.user
            time_entry.story = story
            time_entry.save()
            return {
                'html' : render_to_string('agile/story/time_entry.html', {
                    'time_entry' : time_entry,
                }, RequestContext(request)),
            }
        else:
            story = time_entries[0].story
            story_url = story.get_url()
            return {'story_number': story.number,
                    'story_url': story_url, 
                    'story_name': story.name,
                    }

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
@require_POST
def time_entry(request, project_id, story_number, action=None):
    
    if not request.is_ajax():
        raise Http404
    if action == 'stop':
        time_entries = request.user.time_entries.filter(stop_at=None)
        if time_entries.exists():
            time_entry = time_entries.get()
            time_entry.stop_at = datetime.datetime.now()
            time_entry.save()
            td = time_entry.duration()
            format = "%B %e, %Y, %l:%M %P"
            return {"now": time_entry.stop_at.strftime(format),
                    "id": time_entry.id,
                    "duration": time_entry.duration() 
            }
        else:
            return {"message": "You don't have any time entries to this story"}

@login_required
@render_to_json
def tag(request, project_id, story_number, tag_id, action=None):
    
    if not (request.method == 'POST' and request.is_ajax()):
        raise Http404
    
    project = request.user.projects.get(pk=project_id)
    tag = project.stories.get(number=story_number).tags.get(pk=tag_id)
    
    if action == 'delete':
        tag.delete()