from django.conf.urls.defaults import *

urlpatterns = patterns('agile.views',
    url(r'^$', 'index', name='agile_index'),
    url(r'^login/?$', 'login', name='agile_login'),
    url(r'^logout/?$', 'logout', name='agile_logout'),
    url(r'^signup/?$', 'signup', name='agile_signup'),
    url(r'^profile/?$', 'profile', name='agile_profile'),
    
    url(r'^projects/?$', 'projects', name='agile_projects'),
    url(r'^project/(?P<project_id>\d+)/?$', 'project', name='agile_project'),
    url(r'^project/(?P<project_id>\d+)/details/?$', 'project_details', name='agile_project_details'),
    url(r'^project/(?P<project_id>\d+)/stories/?$', 'project', name='agile_project'),
    url(r'^project/(?P<project_id>\d+)/phases/?$', 'phase', name='agile_phase'),
    url(r'^project/(?P<project_id>\d+)/phase/add/?$', 'add_phase', name='agile_phase_add'),
    url(r'^project/(?P<project_id>\d+)/phase/(?P<phase_id>\d+)/(?P<action>(move|get|edit|delete))/?$', 'phase_ajax', name='agile_phase_ajax'),
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/?$', 'story', name='agile_story'),
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/(?P<action>(move|edit|comment|delete))/?$', 'story_ajax', name='agile_story_ajax'),
    url(r'^project/(?P<project_id>\d+)/story/add/?$', 'story_add', name='agile_story_add'),
    
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/comment/(?P<comment_id>\d+)/(?P<action>(delete|edit))/?$', 'comment', name='agile_comment'),
    
    url(r'^project/(?P<project_id>\d+)/story/(?P<story_number>\d+)/tag/(?P<action>(add|edit|delete|load))(/(?P<tag_id>\d+))?/?$', 'tag', name='agile_tag'),

)


js_info_dict = {
    'packages': ('agile',),
}

urlpatterns += patterns('',
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='agile_js_translations')
)

