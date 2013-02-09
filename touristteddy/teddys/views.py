from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson

from teddys.models import Teddy, Post, Comment

def index(request):
	teddys = Teddy.objects.all()
	template = loader.get_template('teddys/index.html')
	return HttpResponse(template.render(RequestContext(request,{
			'teddys': teddys,
		})))

def detail(request, teddy_id):
	teddy = get_object_or_404(Teddy, pk=teddy_id)
	return render(request, 'teddys/detail.html', {'teddy': teddy})


def teddy_posts(request, teddy_id):
	teddy = get_object_or_404(Teddy, pk=teddy_id)
	return render(request, 'teddys/teddy_posts.html', {'teddy_posts': teddy.post_set.all() })

def teddy_post(request, teddy_id, post_id):
	teddy = get_object_or_404(Teddy, pk=teddy_id)
	return render(request, 'teddys/teddy_posts.html', {'teddy_posts': teddy.post_set.all() })

def post_comments(request, teddy_id, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return HttpResponse(simplejson.dumps(list(post.comment_set.all())), mimetype='application/json')
