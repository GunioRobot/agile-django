from django.conf.urls.defaults import *

urlpatterns = patterns('agile.views',
    url(r'^$', 'index', name='agile_index'),
    url(r'^login/?$', 'login', name='agile_login'),
    url(r'^logout/?$', 'logout', name='agile_logout'),
    url(r'^signup/?$', 'signup', name='agile_signup'),
    url(r'^projects/?$', 'projects', name='agile_projects'),
    url(r'^project/(?P<project_id>\d+)/?$', 'project', name='agile_project'),
    url(r'^profile/?$', 'profile', name='agile_profile'),
    
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/?$', 'story', name='agile_story'),
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/edit/?$', 'story', name='agile_story_edit'),
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/move/?$', 'story', name='agile_story_move'),


)
