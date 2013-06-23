import datetime
from django.core import serializers
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from django.utils import simplejson, timezone
from touristteddy import utils
from teddys.models import Teddy, Post, Comment
import json


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
    comments = post.comment_set.all().order_by("-comment_time")
    comment_dictionary = [{
                          'comment': c.comment,
                          'comment_time': utils.get_friendly_time(c.comment_time),
                          'user_id': c.user.id,
                          'user_name': c.user.username,

                          } for c in comments]
    data = json.dumps(comment_dictionary)
    return HttpResponse(data, mimetype='application/json')


def post_comment2(request, teddy_id, post_id):
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


def post_comment(request, teddy_id, post_id):
    request_comment = json.loads(request.body)
    comment = Comment()
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=post_id)
        comment.comment = request_comment['comment']
        comment.comment_time = datetime.datetime.now()
        comment.post = post
        comment.user = request.user
        comment.save()

    comment_time_tz_aware = timezone.make_aware(comment.comment_time, timezone.get_default_timezone())
    json_comment = {
        'comment': comment.comment,
        'comment_time': utils.get_friendly_time(comment_time_tz_aware),
        'user_id': comment.user.id,
        'user_name': comment.user.username
    }

    return HttpResponse(json.dumps(json_comment), mimetype='application/json')


def add_post(request, teddy_id):
    request_post = json.loads(request.body)
    post = Post()

    title = ''
    description = ''
    picture = ''
    latitude = ''
    longitude = ''
    teddy_id = ''

    if request.user.is_authenticated():
        title = request_post['title']
        description = request_post['description']
        # picture = request.FILES['picture']
        # picture_file = picture.read()
        # medium_picture = ContentFile(utils.rescale(picture_file, int(700), int(650), False))
        # small_picture = ContentFile(utils.rescale(picture_file, int(280), int(187), True))
        # file_name = picture.name.split('.')[0]
        # file_ending = picture.name.split('.')[1]
        # medium_picture.name = '{0}_medium.{1}'.format(file_name, file_ending)
        # small_picture.name = '{0}_small.{1}'.format(file_name, file_ending)
        # utils.handle_uploaded_file(medium_picture)
        # utils.handle_uploaded_file(small_picture)
        latitude = request_post['latitude']
        longitude = request_post['longitude']
        teddy_id = request_post['teddy_id']
        teddy = get_object_or_404(Teddy, pk=teddy_id)
        post = Post(title=title,
                    description=description,
                    #picture=medium_picture,
                    # small_picture=small_picture,
                    latitude=latitude,
                    longitude=longitude,
                    teddy=teddy,
                    user=request.user)
        #post.save()

    json_post = {
        'title': post.title,
        'description': post.description,
        'latitude': post.latitude,
        'longitude': post.longitude,
        'teddy_id': post.teddy_id,
        'user_name': post.user.username
    }

    return HttpResponse(json.dumps(json_post), mimetype='application/json')


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

