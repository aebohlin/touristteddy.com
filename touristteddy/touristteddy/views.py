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

def new_user(request):
    state = "Fill out the form below..."
    username = password = password_again = first_name = last_name = email = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        redirect_to = request.POST.get('next', '')
        
        user = User()

        if username == '':
            state = 'Please fill out username'
        elif password == '':
            state = 'Please fill out password'
        elif password != password_again:
            state = 'Passwords do not match'
        elif utils.validate_email_address(email) == False:
            state = 'Email is not valid'
        else: 
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            index(request)
            state = "User created!"
            return HttpResponseRedirect(redirect_to)  

    return render_to_response('newuser.html',{
        'state':state, 
        'username': username, 
        'first_name': first_name, 
        'last_name': last_name, 
        'email': email, 
        'next': request.REQUEST.get('next', '')
    }, context_instance=RequestContext(request))


def get_user_as_json(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    data = serializers.serialize("json", user)
    return HttpResponse({ "user": data } , mimetype='application/json')