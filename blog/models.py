from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BlogUser(AbstractUser):
	can_post = models.BooleanField(default=False)
	
class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=256)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	
	def publish(self):
		self.published_date = timezone.now()
		self.save()
		
	def unpublish(self):
		self.published_date = None
		self.save()
		
	def __str__(self):
		return self.title
	
class Comment(models.Model):
	post = models.ForeignKey(Post)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	text = models.TextField()
	published_date = timezone.now()
	
	def __str__(self):
		return textwrap.shorten(text, width=256, placeholder='...')