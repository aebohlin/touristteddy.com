from django.http import HttpResponse
from django.template import Context, loader

from teddys.models import Teddy, Post

def index(request):
	teddys = Teddy.objects.all()
	template = loader.get_template('teddys/index.html')
	return HttpResponse(Context({
			'teddys': teddys,
		}))
