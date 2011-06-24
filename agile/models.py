from django.db import models, transaction
from django.db.models import F, Max
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

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
    
    def get_base_url(self):
        return '/'.join(self.get_url().split('/')[:-1])

    def get_url(self):
        return reverse('agile_project', args=[self.id])
    
    def get_details_url(self):
        return reverse('agile_project_details', args=[self.id])
    
    def get_phases_url(self):
        return reverse('agile_phase', args=[self.id])
    
    @property
    def stories(self):
        return Story.objects.filter(phase__project=self)
    
    @property
    def users(self):
        return (self.members.all() | User.objects.filter(id=self.owner.id)).distinct() 
    
class Phase(models.Model):
    project = models.ForeignKey('Project', verbose_name=_(u'project'), related_name='phases')
    name = models.CharField(_(u'name'), max_length=30)
    index = models.PositiveIntegerField(_(u'index'))
    description = models.CharField(_(u'description'), max_length=100, blank=True)
    stories_limit = models.PositiveIntegerField(_(u'stories limit'), blank=True, null=True)
    is_backlog = models.BooleanField(_(u'is backlog'), default=False)
    is_archive = models.BooleanField(_(u'is archive'), default=False)
    
    class Meta:
        verbose_name = _(u'phase')
        verbose_name_plural = _(u'phases')
        ordering = ('-is_backlog', 'is_archive', 'index')
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    @property
    def is_deletable(self):
        return not self.is_backlog_or_archive
    
    @property
    def is_backlog_or_archive(self):
        return self.is_backlog or self.is_archive
    
    @transaction.commit_on_success()
    def move(self, new_index):
        new_index = int(new_index)
        phases = self.project.phases
        if new_index < self.index:
                phases.filter(
                    index__lt=self.index,
                    index__gte=new_index
                ).update(index=F('index') + 1)
        elif new_index > self.index:
            phases.filter(
                index__gt=self.index,
                index__lte=new_index
            ).update(index=F('index') - 1)
        else:
            # Same index, we don't to save anything.
            return
        
        self.index = new_index
        self.save()

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
    ready = models.BooleanField(default=False)
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
    
    def get_add_comment_url(self):
        return reverse('agile_story_ajax', args=[self.project_id, self.number, 'comment'])
    
    @transaction.commit_on_success()
    def move(self, new_phase_id, new_index=None):
        """
        This method moves a Story through the phases
        including the index management.
        
         - If the new Phase and the new index are the same
           as the current, do nothing.
        
         - If the new Phase is the same as the current one, just
           changes the index.
        
         - If the new Phase is another one than the current,
           changes the index and the Phase which this belongs,
           and manages all the index needed stuff.
        
         - If new index is not given or is None and the new Phase
           given is another one than the current, moves the Story at
           the end of the new Phase.
        """
        stories = self.phase.stories.all()
        # Same phase id, so we give space to the new
        # story in the same phase.
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
        else:
            stories.filter(index__gt=self.index).update(index=F('index') - 1)
            self.phase_id = new_phase_id
            
            # Let's calculate the max + 1 index
            if new_index is None:
                max = Story.objects.filter(
                    phase=new_phase_id).aggregate(max=Max('index'))['max']
                new_index = 0 if max is None else max + 1
            
            # Move the stories index + 1 for give space to the new story
            else:
                Story.objects.filter(
                    phase=new_phase_id,
                    index__gte=new_index
                ).update(index=F('index') + 1)

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
        
    @transaction.commit_on_success()
    def delete(self, *args, **kwargs):
        super(Story, self).delete(*args, **kwargs)
        # FIXME: this code is being repeated
        stories = self.phase.stories.all()
        stories.filter(index__gt=self.index).update(index=F('index') - 1)
    
class Tag(models.Model):
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='tags')
    name = models.CharField(_(u'name'), max_length=100)
    
    class Meta:
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags')

class TaskManager(models.Manager):
    
    def finished(self):
        return self.filter(finished_at__isnull=False)
    
    def get_percentage_finished(self):
        total = float(self.all().count())
        finished = float(self.finished().count())
        
        if total:     
            return '%.2f%%' % (finished / total * 100)
        else:
            return '0.00%'
        
    def get_formatted_count(self):
        total = self.count()
        if total:
            return _(u'%s of %s') % (self.finished().count(), total)
        else:
            return '0'
    
class Task(models.Model):
    index = models.PositiveIntegerField(_(u'index'))
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='tasks')
    description = models.CharField(_(u'description'), max_length=512)
    finished_at = models.DateTimeField(_(u'finished at'), blank=True, null=True)
    finished_by = models.ForeignKey(User, verbose_name=_(u'user'), related_name='finished_tasks', blank=True, null=True)
    
    objects = TaskManager()
      
    class Meta:
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')
        ordering = ('index',)
    
class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='comments')
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='comments')
    datetime = models.DateTimeField(_(u'datetime'), auto_now=True)
    text = models.TextField(_(u'text'))
        
    class Meta:
        verbose_name = _(u'comment')
        verbose_name_plural = _(u'comments')
        ordering = ('datetime',)

class Attachment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'user'), related_name='attachments')
    story = models.ForeignKey('Story', verbose_name=_(u'story'), related_name='attachments')
    description = models.CharField(_(u'description'), max_length=50)
    datetime = models.DateTimeField(_(u'datetime'), auto_now=True)
    file = models.FileField(upload_to='attachments')
        
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
    user_language = models.CharField(_(u'user language'), max_length=2, default=None, choices=settings.LANGUAGES, null=True, blank=True)
        
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

def agile_get_name(user):
    return user.get_full_name() or user.username.title()
User.agile_get_name = agile_get_name

################################################################################
## Signals
################################################################################

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user=instance).save()

post_save.connect(create_user_profile, sender=User)
        
def create_project(sender, instance, created, **kwargs):
    if created:
        # We need the no lazy ugettext here.
        from django.utils.translation import ugettext as _
        phases = instance.phases
        phases.create(
            index=0,
            name=_(u'Backlog'),
            description=_(u'Stories that will be worked on someday'),
            is_backlog=True,
        )
        phases.create(
            index=1,
            name=_(u'Ready'),
            description=_(u'Stories that are ready to be worked on'),
        )
        phases.create(
            index=2,
            name=_(u'Working'),
            description=_(u'Stories that are currently being worked on'),
        )
        phases.create(
            index=3,
            name=_(u'Complete'),
            description=_(u'Stories that have been completed'),
        )
        phases.create(
            index=4,
            name=_(u'Archive'),
            description=_(u'Stories that are history'),
            is_archive=True,
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
