from django.conf.urls.defaults import *

urlpatterns = patterns('agile.views',
    url(r'^$', 'index', name='agile_index'),
    url(r'^login/?$', 'login', name='agile_login'),
    url(r'^logout/?$', 'logout', name='agile_logout'),
    url(r'^signup/?$', 'signup', name='agile_signup'),
    url(r'^projects/?$', 'projects', name='agile_projects'),
    # Example:
    # (r'^django_agile/', include('django_agile.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
