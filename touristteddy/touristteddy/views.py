from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from teddys.models import Teddy, Post
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.contrib.auth.models import User
from touristteddy import utils

def index(request):
	teddys = Teddy.objects.all()
	posts = Post.objects.all()
	template = loader.get_template('index.html')

#c = RequestContext(request, {'message': 'I am view 1.'},
 #           processors=[custom_proc])
	return HttpResponse(template.render(RequestContext(request, {
		'teddys': teddys,
		'posts': posts,
        'username': utils.get_username_or_fullname(request.user)
		})))
	#return HttpResponse(template.render(Context({
	#	'teddys': teddys,
	#	'posts': posts,
	#	})))

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect_to = request.POST.get('next', '')
		
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                index(request)
                state = "You're successfully logged in!"
                return HttpResponseRedirect(redirect_to)  
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Incorrent username and/or password."

    return render_to_response('auth.html',{'state':state, 'username': username, 'next': request.REQUEST.get('next', '')}, context_instance=RequestContext(request))


def get_user_as_json(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    data = serializers.serialize("json", user)
    return HttpResponse({ "user": data } , mimetype='application/json')