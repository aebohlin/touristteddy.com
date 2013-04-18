import datetime
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.utils import simplejson
from touristteddy import utils
from teddys.models import Teddy, Post, Comment


def index(request):
    teddys = Teddy.objects.all()
    template = loader.get_template('teddys/index.html')
    return HttpResponse(template.render(RequestContext(request, {
        'teddys': teddys,
    })))


def detail(request, teddy_id):
    teddy = get_object_or_404(Teddy, pk=teddy_id)
    return render(request, 'teddys/detail.html', {'teddy': teddy})


def teddy_posts(request, teddy_id):
    teddy = get_object_or_404(Teddy, pk=teddy_id)
    return render(request, 'teddys/teddy_posts.html', {'teddy_posts': teddy.post_set.all()})


def teddy_post(request, teddy_id, post_id):
    teddy = get_object_or_404(Teddy, pk=teddy_id)
    return render(request, 'teddys/teddy_posts.html', {'teddy_posts': teddy.post_set.all()})


def post_comments_as_json(request, teddy_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = []
    for comment in post.comment_set.all().order_by("-comment_time"):
        comments.append([comment.comment,
                         utils.get_username_or_fullname(comment.user),
                         comment.user.id,
                         utils.get_friendly_time(comment.comment_time)])

    data = simplejson.dumps(comments)
    return HttpResponse(data, mimetype='application/json')


def post_comment(request, teddy_id, post_id):
    success = False
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=post_id)
        comment = Comment()
        comment.comment = request.POST.get('comment')
        comment.comment_time = datetime.datetime.now()
        comment.post = post
        comment.user = request.user
        comment.save()
        success = True
    return HttpResponse(simplejson.dumps(success), mimetype='application/json')


def create_post(request):
    title = ''
    description = ''
    picture = ''
    lat = ''
    lng = ''
    teddy_id = ''

    if request.POST and request.user.is_authenticated():
        title = request.POST.get('title')	
        description = request.POST.get('description')
        picture = request.FILES['picture']
        picture_file = picture.read()
        medium_picture = ContentFile(utils.rescale(picture_file, int(700), int(650), False))
        small_picture = ContentFile(utils.rescale(picture_file, int(280), int(187), True))
        file_name = picture.name.split('.')[0]
        file_ending = picture.name.split('.')[1]
        medium_picture.name = '{0}_medium.{1}'.format(file_name, file_ending)
        small_picture.name = '{0}_small.{1}'.format(file_name, file_ending)
        utils.handle_uploaded_file(medium_picture)
        utils.handle_uploaded_file(small_picture)
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        teddy_id = request.POST.get('teddy_id')
        teddy = get_object_or_404(Teddy, pk=teddy_id)
        post = Post(title=title,
                    description=description,
                    picture=medium_picture,
                    small_picture=small_picture,
                    latitude=lat,
                    longitude=lng,
                    teddy=teddy,
                    user=request.user)
        post.save()

    return render_to_response('teddys/create_post.html', {
        'title': title,
        'description': description,
        'picture': picture,
        'lat': lat,
        'lng': lng,
        'teddy_id': teddy_id
    }, context_instance=RequestContext(request))

