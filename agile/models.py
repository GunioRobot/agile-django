from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as __, ugettext_lazy as _

# Create your models here.

class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=100)
    description = models.TextField(_(u'description'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_(u'owner'), related_name='projects')
    members = models.ManyToManyField(User, verbose_name=_(u'members'), blank=True)
    
    class Meta:
        verbose_name = _(u'project')
        verbose_name_plural = _(u'projects')
    
    def __unicode__(self):
        return '%s' % self.name
    
    def get_url(self):
        return 'project/%s' % self.id
    
class Process(models.Model):
    project = models.ForeignKey('Project', verbose_name=_(u'project'), related_name='columns')
    index = models.PositiveIntegerField(_(u'index'))
    name = models.CharField(_(u'name'), max_length=100)
    
    class Meta:
        verbose_name = _(u'process')
        verbose_name_plural = _(u'processes')

#class Sprint(models.Model):    
	
class Story(models.Model):
    #project = models.ForeignKey('Project', related_name='stories') # Unnecesary?
    process = models.ForeignKey('Process', verbose_name=_(u'process'), related_name='stories')
    number = models.PositiveIntegerField(_(u'number'))
    name = models.CharField(_(u'name'), max_length=100)
    description = models.TextField(_(u'description'), blank=True)
    creator = models.ForeignKey(User, verbose_name=_(u'creator'), related_name='created_stories', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name=_(u'owner'), related_name='owned_stories', blank=True, null=True)
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    blocked = models.CharField(max_length=100)
    color = models.CharField(_(u'color'), max_length=6, default='ffffff')
    
    class Meta:
        verbose_name = _(u'story')
        verbose_name_plural = _(u'stories')
    
class Task(models.Model):
    index = models.PositiveIntegerField(_(u'index'))
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='tasks')
    description = models.TextField(_(u'description'))
    finished_at = models.DateTimeField(_(u'finished at'), blank=True)
      
    class Meta:
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='comments')
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='comments')
    datetime = models.DateTimeField(_(u'datetime'), auto_now=True)
    text = models.CharField(_(u'text'), max_length=100)
        
    class Meta:
        verbose_name = _(u'comment')
        verbose_name_plural = _(u'comments')

class Attachment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='attachments')
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='attachments')
    datetime = models.DateTimeField(_(u'datetime'), auto_now=True)
    file = models.CharField(max_length=100)
        
    class Meta:
        verbose_name = _(u'attachment')
        verbose_name_plural = _(u'attachments')

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(u'user'))
        
    class Meta:
        verbose_name = _(u'user profile')
        verbose_name_plural = _(u'user profiles')

class Filter(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='filters')
    name = models.CharField(_(u'name'), max_length=100)
    query = models.CharField(_(u'query'), max_length=100)
    shared = models.BooleanField(_(u'shared'), default=True)
        
    class Meta:
        verbose_name = _(u'filter')
        verbose_name_plural = _(u'filters')
	
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()
        
def create_project(sender, instance, created, **kwargs):
    if created:
        Process(
            project=instance,
            index=0,
            name=__(u'Backlog'),
        ).save()
        
        Process(
            project=instance,
            index=1,
            name=__(u'Ready'),
        ).save()
        
        Process(
            project=instance,
            index=2,
            name=__(u'Working'),
        ).save()
        
        Process(
            project=instance,
            index=3,
            name=__(u'Complete'),
        ).save()
        
        Process(
            project=instance,
            index=4,
            name=__(u'Archive'),
        ).save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_project, sender=Project)