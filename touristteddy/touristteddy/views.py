from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from teddys.models import Teddy, Post

def index(request):
	teddys = Teddy.objects.all()
	posts = Post.objects.all()
	template = loader.get_template('index.html')

#c = RequestContext(request, {'message': 'I am view 1.'},
 #           processors=[custom_proc])
	return HttpResponse(template.render(RequestContext(request, {
		'teddys': teddys,
		'posts': posts,
		})))
	#return HttpResponse(template.render(Context({
	#	'teddys': teddys,
	#	'posts': posts,
	#	})))

