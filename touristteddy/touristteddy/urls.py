from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults import *

from touristteddy import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

	url(r'^$', views.index, name='index'),
    # url(r'^$', 'touristteddy.views.home', name='home'),
    # url(r'^touristteddy/', include('touristteddy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teddys/', include('teddys.urls')),
    url(r'^login/$', 'touristteddy.views.login_user'),
    url(r'^newuser/$', 'touristteddy.views.new_user'),
    url(r'^users/(?P<user_id>\d+)/json/$', 'touristteddy.views.get_user_as_json'),
    url(r'^create_post/$', 'teddys.views.create_post'),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
