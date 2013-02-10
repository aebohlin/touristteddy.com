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

	def get_friendly_comment_time(self):
		friendly_comment_time = self.comment_time.strftime('%Y-%m-%d');
		#now = datetime.datetime.now()
		now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
		if self.comment_time > now - datetime.timedelta(seconds=30):
			friendly_comment_time = "now"
		elif self.comment_time > now - datetime.timedelta(minutes=1):
			friendly_comment_time = "less than a minute ago"
		elif self.comment_time > now - datetime.timedelta(minutes=60):
			minutes = ((now - self.comment_time) / 60).seconds
			friendly_comment_time = str(minutes) 
			if minutes == 1:
				friendly_comment_time += " minute ago"
			else:
				friendly_comment_time += " minutes ago"
		elif self.comment_time > now - datetime.timedelta(hours=24):
			hours = ((now - self.comment_time) / 3600).seconds
			friendly_comment_time = str(hours) 
			if hours == 1:
				friendly_comment_time += " hour ago"
			else:
				friendly_comment_time += " hours ago"
		elif self.comment_time > now - datetime.timedelta(days=7):
			days = ((now - self.comment_time) / (3600 * 24)).seconds
			friendly_comment_time = str(days) 
			if days == 1:
				friendly_comment_time += " day ago"
			else:
				friendly_comment_time += " days ago"

		return friendly_comment_time