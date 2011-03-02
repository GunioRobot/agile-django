from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
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
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='created_stories')
    owner = models.ForeignKey(User, related_name='owned_stories')
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.CharField(max_length=100)
    color = models.CharField(max_length=6)
    
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
    shared = models.BooleanField(default=False)
	
