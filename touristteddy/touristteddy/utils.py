import datetime
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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

def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def handle_uploaded_file(f):
    #destination = open('/tmp/'+file.name, 'wb+')
    with open('/tmp/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def rescale(data, width, height, force=True):
    """Rescale the given image, optionally cropping it to make sure the result image has the specified width and height."""
    from cStringIO import StringIO

    max_width = width
    max_height = height

    input_file = StringIO(data)
    img = pil.open(input_file)
    
    if not force:
        img.thumbnail((max_width, max_height), pil.ANTIALIAS)
    else:
        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)
        
        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 3
            
        img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
        img = img.resize((dst_width, dst_height), pil.ANTIALIAS)
        
    tmp = StringIO()
    img.save(tmp, 'JPEG')
    tmp.seek(0)
    output_data = tmp.getvalue()
    input_file.close()  
    
    return output_data
