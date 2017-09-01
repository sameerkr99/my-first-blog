from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blogproject import settings
# Create your models here.
class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 100)
	text = models.TextField()
	create_date = models.DateTimeField(default = timezone.now)
	publish_date = models.DateTimeField(blank = True,null = True)
	like = models.IntegerField(default = 0)
	image = models.FileField(null=True, upload_to=settings.MEDIA_ROOT+'/postsimages/')
	commentcount = models.IntegerField(default=0)
	category = models.ForeignKey('myblog.Categories')
	def __str__(self):
		return self.title


class Categories(models.Model):
	title = models.CharField(max_length = 20)
	def __str__(self):
		return self.title

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, null = True)
	dp = models.FileField(default = 'profilepic/default/default_dp.png')
	phone = models.CharField(max_length = 10)
	birth = models.DateField(null = True, blank = True)
	def __str__(self):
		return str(self.user)
	def save(self):
		for field in self._meta.fields:
			if field.name == 'dp':
				field.upload_to= settings.MEDIA_ROOT+"/profilepic/%s" % self.user
		super(Profile, self).save()
class comments(models.Model):
	post = models.ForeignKey('myblog.Post')
	authorprofile = models.ForeignKey('myblog.Profile')
	comment = models.CharField(max_length=100)
	def __str__(self):
		return str(self.post)

class Upvotes(models.Model):
	post = models.ForeignKey('myblog.Post')
	user = models.ForeignKey('auth.User')
	upvote = models.BooleanField(default = False)
	def __str__(self):
		return str(self.post)