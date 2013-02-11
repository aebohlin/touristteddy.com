from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Teddy(models.Model):
	unique_id = models.CharField(max_length=200)
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	picture = models.ImageField(upload_to='posts', max_length=100)
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	teddy = models.ForeignKey(Teddy)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	comment = models.TextField()
	comment_time = models.DateTimeField()
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return self.comment