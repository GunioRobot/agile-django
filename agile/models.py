from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext as __, ugettext_lazy as _

class AgileModelException(Exception):
    pass

################################################################################
## Models
################################################################################

class Project(models.Model):
    name = models.CharField(_(u'name'), max_length=100)
    description = models.TextField(_(u'description'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_(u'owner'), related_name='own_projects')
    members = models.ManyToManyField(User, verbose_name=_(u'members'), related_name='member_projects', blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _(u'project')
        verbose_name_plural = _(u'projects')
    
    def __unicode__(self):
        return '%s' % self.name
    
    def get_url(self):
        return reverse('agile_project', args=[self.id])
    
    @property
    def stories(self):
        return Story.objects.filter(phase__project=self) 
    
class Phase(models.Model):
    project = models.ForeignKey('Project', verbose_name=_(u'project'), related_name='phases')
    name = models.CharField(_(u'name'), max_length=100)
    index = models.PositiveIntegerField(_(u'index'))
    description = models.TextField(_(u'description'), blank=True)
    limit = models.PositiveIntegerField(_(u'limit'), blank=True, null=True)
    deletable = models.BooleanField(_(u'deletable'), default=True)
    
    class Meta:
        verbose_name = _(u'phase')
        verbose_name_plural = _(u'phases')
    
    def __unicode__(self):
        return 'project: %s , phase: %s' % (self.project, self.name)

#class Sprint(models.Model):    
	
class Story(models.Model):
    phase = models.ForeignKey('Phase', verbose_name=_(u'phase'), related_name='stories')
    number = models.PositiveIntegerField(_(u'number'))
    name = models.CharField(_(u'name'), max_length=100)
    description = models.TextField(_(u'description'), blank=True)
    creator = models.ForeignKey(User, verbose_name=_(u'creator'), related_name='created_stories', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name=_(u'owner'), related_name='own_stories', blank=True, null=True)
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    blocked = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(_(u'color'), max_length=6, default='ffffff')
    
    class Meta:
        verbose_name = _(u'story')
        verbose_name_plural = _(u'stories')
        
    @property
    def project(self):
        return self.phase.project
    
class Tag(models.Model):
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='tags')
    name = models.CharField(_(u'name'), max_length=100)
    
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
    user = models.OneToOneField(User, verbose_name=_(u'user'), related_name='agile_userprofile')
        
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

# Extending User model
User.projects = property(lambda u: (u.own_projects.all() | u.member_projects.all()).distinct())

################################################################################
## Signals
################################################################################

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()

post_save.connect(create_user_profile, sender=User)
        
def create_project(sender, instance, created, **kwargs):
    if created:
        instance.phases.create(
            index=0,
            name=__(u'Backlog'),
            deletable=False,
        )
        instance.phases.create(
            index=1,
            name=__(u'Ready'),
        )
        instance.phases.create(
            index=2,
            name=__(u'Working'),
        )
        instance.phases.create(
            index=3,
            name=__(u'Complete'),
        )
        instance.phases.create(
            index=4,
            name=__(u'Archive'),
            deletable=False,
        )
        
post_save.connect(create_project, sender=Project)

def delete_phase(sender, instance, **kwargs):
    if not instance.deletable:
        raise AgileModelException('This phase is not deletable')
    
    if instance.stories.all().exists():
        raise AgileModelException('This phase has stories')

pre_delete.connect(delete_phase, sender=Phase)
