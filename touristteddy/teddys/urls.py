from django.conf.urls import patterns, url

from teddys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<teddy_id>\d+)/$', views.detail, name='detail')
)