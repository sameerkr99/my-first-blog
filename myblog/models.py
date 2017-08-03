from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blogproject import settings
# Create your models here.
class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 50)
	text = models.TextField()
	create_date = models.DateTimeField(default = timezone.now)
	publish_date = models.DateTimeField(blank = True,null = True)
	like = models.IntegerField(default = 0)
	def __str__(self):
		return self.title


class Categories(models.Model):
	title = models.CharField(max_length = 20)
	def __str__(self):
		return self.title

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, null = True)
	dp = models.ImageField(upload_to= settings.STATIC_ROOT+"/profilepic")
	Phone = models.CharField(max_length = 10)
	birth = models.DateField(null = True, blank = True)
	def __str__(self):
		return str(self.user)

class comments(models.Model):
	post = models.ForeignKey('myblog.Post')
	author = models.CharField(default = "user", max_length = 20)
	comment = models.CharField(max_length=100)
	def __str__(self):
		return str(self.post)
