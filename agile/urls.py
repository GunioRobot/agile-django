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
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/(?P<action>(move|edit|comment|delete))/?$', 'story_ajax', name='agile_story_ajax'),
    url(r'^project/(?P<project_id>\d+)/story/add/?$', 'story_add', name='agile_story_add'),
    
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/comment/(?P<comment_id>\d+)/(?P<action>(delete|edit))/?$', 'comment', name='agile_comment'),

)


js_info_dict = {
    'packages': ('agile',),
}

urlpatterns += patterns('',
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='agile_js_translations')
)

