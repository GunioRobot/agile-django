from django.db import models, transaction
from django.db.models import F, Max
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _

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
    
    @property
    def users(self):
        return (self.members.all() | User.objects.filter(id=self.owner.id)).distinct() 
    
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
        ordering = ('index',)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
#class Sprint(models.Model):    
	
class Story(models.Model):
    number = models.PositiveIntegerField(_(u'number'))
    index = models.PositiveIntegerField(_(u'index'))
    name = models.CharField(_(u'name'), max_length=100)
    description = models.TextField(_(u'description'), blank=True)
    phase = models.ForeignKey('Phase', verbose_name=_(u'phase'), related_name='stories')
    creator = models.ForeignKey(User, verbose_name=_(u'creator'), related_name='created_stories', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name=_(u'owner'), related_name='own_stories', blank=True, null=True)
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    blocked = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(_(u'color'), max_length=6, default='ffffff')
    
    class Meta:
        verbose_name = _(u'story')
        verbose_name_plural = _(u'stories')
        ordering = ('index',)
    
    def __unicode__(self):
        return '%s, Index %s, name %s' % (self.phase, self.index, self.name)
    
    @property
    def project(self):
        return self.phase.project
    
    @property
    def project_id(self):
        return self.phase.project_id
    
    def get_url(self):
        return reverse('agile_story', args=[self.project_id, self.number])
    
    @transaction.commit_on_success()
    def move(self, new_phase_id, new_index):
        stories = self.phase.stories.all()
        if new_phase_id == self.phase_id:
            if new_index < self.index:
                stories.filter(
                    index__lt=self.index,
                    index__gte=new_index
                ).update(index=F('index') + 1)
            elif new_index > self.index:
                stories.filter(
                    index__gt=self.index,
                    index__lte=new_index
                ).update(index=F('index') - 1)
            else:
                # Same phase, same index, we don't to save anything.
                return
        elif new_index is not None:
            stories.filter(index__gt=self.index).update(index=F('index') - 1)
            Story.objects.filter(
                phase=new_phase_id,
                index__gte=new_index
            ).update(index=F('index') + 1)
            self.phase_id = new_phase_id
        elif new_index is None:
            new_index = (Story.objects.filter(
                phase=new_phase_id).aggregate(max=Max('index'))['max'] or 0) + 1
            self.phase_id = new_phase_id
        self.index = new_index
        self.save()
        
    @transaction.commit_on_success()
    def save(self, *args, **kwargs):
        # If is a new Story instance
        if self.id is None:
            project = self.phase.project
            self.number = (project.phases.aggregate(max=Max('stories__number'))['max'] or 0) + 1
            self.index = (self.phase.stories.aggregate(max=Max('index'))['max'] or 0) + 1
        super(Story, self).save(*args, **kwargs)
    
class Tag(models.Model):
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='tags')
    name = models.CharField(_(u'name'), max_length=100)
    
    class Meta:
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags')
    
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

JQUERY_UI_THEMES = (
   #('base', 'base'),
   ('black-tie', 'Black Tie'),
   ('blitzer', 'Blitzer'),
   ('cupertino', 'Cupertino'),
   ('dark-hive', 'Dark Hive'),
   ('dot-luv', 'Dot Luv'),
   ('eggplant', 'Eggplant'),
   ('excite-bike', 'Excite Bike'),
   ('flick', 'Flick'),
   ('hot-sneaks', 'Hot sneaks'),
   ('humanity', 'Humanity'),
   ('le-frog', 'Le Frog'),
   ('mint-choc', 'Mint Choc'),
   ('overcast', 'Overcast'),
   ('pepper-grinder', 'Pepper Grinder'),
   ('redmond', 'Redmond'),
   ('smoothness', 'Smoothness'),
   ('south-street', 'South Street'),
   ('start', 'Start'),
   ('sunny', 'Sunny'),
   ('swanky-purse', 'Swanky Purse'),
   ('trontastic', 'Trontastic'),
   ('ui-darkness', 'UI darkness'),
   ('ui-lightness', 'UI lightness'),
   ('vader', 'Vader'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_(u'user'), related_name='agile_userprofile')
    jquery_ui_theme = models.CharField(_(u'jQuery UI Theme'), max_length=100, default='cupertino', choices=JQUERY_UI_THEMES)
        
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
@property
def projects(user):
    return (user.own_projects.all() | user.member_projects.all()).distinct()
User.projects = projects

################################################################################
## Signals
################################################################################

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()

post_save.connect(create_user_profile, sender=User)
        
def create_project(sender, instance, created, **kwargs):
    if created:
        from django.utils.translation import ugettext as _
        phases = instance.phases
        phases.create(
            index=0,
            name=_(u'Backlog'),
            deletable=False,
        )
        phases.create(
            index=1,
            name=_(u'Ready'),
        )
        phases.create(
            index=2,
            name=_(u'Working'),
        )
        phases.create(
            index=3,
            name=_(u'Complete'),
        )
        phases.create(
            index=4,
            name=_(u'Archive'),
            deletable=False,
        )
        
post_save.connect(create_project, sender=Project)

#def delete_phase(sender, instance, **kwargs):
#    if not instance.deletable:
#        raise AgileModelException('This phase is not deletable')
#
#    if instance.stories.all().exists():
#        raise AgileModelException('This phase has stories')
#
#pre_delete.connect(delete_phase, sender=Phase)
