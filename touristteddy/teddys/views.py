from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404

from teddys.models import Teddy, Post

def index(request):
	teddys = Teddy.objects.all()
	template = loader.get_template('teddys/index.html')
	return HttpResponse(template.render(Context({
			'teddys': teddys,
		})))

def detail(request, teddy_id):
	teddy = get_object_or_404(Teddy, pk=teddy_id)
	return render(request, 'teddys/detail.html', {'teddy': teddy})