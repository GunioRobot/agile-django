from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, related_name='projects')
    members = models.ManyToManyField(User, blank=True)
    
class Column(models.Model):
    project = models.ForeignKey('Project', related_name='columns')
    index = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

#class Sprint(models.Model):    
	
class Story(models.Model):
    #project = models.ForeignKey('Project', related_name='stories') # Unnecesary?
    column = models.ForeignKey('Column', related_name='stories')
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, related_name='created_stories', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owned_stories', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.CharField(max_length=100)
    color = models.CharField(max_length=6, default='ffffff')
    
    class Meta:
		verbose_name_plural = 'stories'
    
class Task(models.Model):
    index = models.PositiveIntegerField()
    story = models.ForeignKey('Story', related_name='tasks')
    description = models.TextField()
    finished_at = models.DateTimeField(blank=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments')
    story = models.ForeignKey('Story', related_name='comments')
    datetime = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=100)

class Attachment(models.Model):
    user = models.ForeignKey(User, related_name='attachments')
    story = models.ForeignKey('Story', related_name='attachments')
    datetime = models.DateTimeField(auto_now=True)
    file = models.CharField(max_length=100)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

class Filter(models.Model):
    user = models.ForeignKey(User, related_name='filters')
    name = models.CharField(max_length=100)
    query = models.CharField(max_length=100)
    shared = models.BooleanField(default=True)
	
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()

post_save.connect(create_user_profile, sender=User)