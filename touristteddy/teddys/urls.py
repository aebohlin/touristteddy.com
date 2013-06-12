from django.conf.urls import patterns, url

from teddys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<teddy_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<teddy_id>\d+)/posts/$', views.teddy_posts, name='teddy_posts'),
	url(r'^(?P<teddy_id>\d+)/posts/(?P<post_id>\d+)/$', views.teddy_post, name='teddy_posts'),
	url(r'^(?P<teddy_id>\d+)/posts/(?P<post_id>\d+)/comments/json$', views.post_comments_as_json, name='post_comments_as_json'),
	url(r'^(?P<teddy_id>\d+)/posts/(?P<post_id>\d+)/comments/add$', views.post_comment, name='post_comment'),
	url(r'^(?P<teddy_id>\d+)/posts/add$', views.add_post, name='add_post'),
)
