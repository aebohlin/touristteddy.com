import datetime
from django.utils import timezone

def get_username_or_fullname(user):
	# trys to get users fullname, returns username if fullname is empty
	username = ""
	if user.is_authenticated(): 
		username = "%s %s" % (user.first_name, user.last_name)
		if username == " ":
			username = user.username
	return username

def get_friendly_time(time):
	friendly_time = time.strftime('%Y-%m-%d');
	now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
	if time > now - datetime.timedelta(seconds=30):
		friendly_time = "now"
	elif time > now - datetime.timedelta(minutes=1):
		friendly_time = "less than a minute ago"
	elif time > now - datetime.timedelta(minutes=60):
		minutes = ((now - time) / 60).seconds
		friendly_time = str(minutes) 
		if minutes == 1:
			friendly_time += " minute ago"
		else:
			friendly_time += " minutes ago"
	elif time > now - datetime.timedelta(hours=24):
		hours = ((now - time) / 3600).seconds
		friendly_time = str(hours) 
		if hours == 1:
			friendly_time += " hour ago"
		else:
			friendly_time += " hours ago"
	elif time > now - datetime.timedelta(days=7):
		days = ((now - time) / (3600 * 24)).seconds
		friendly_time = str(days) 
		if days == 1:
			friendly_time += " day ago"
		else:
			friendly_time += " days ago"

	return friendly_time