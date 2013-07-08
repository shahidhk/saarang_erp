from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Forum(models.Model):
    '''
        Defines the Forum class ie. the department Forums
    '''
    title = models.CharField(max_length=60,unique=True) # Title
    department=models.CharField(max_length=60,choices=settings.DEPARTMENTS)
    #position = models.IntegerField('Position', blank=True, default=0) #Defines the position of the forum
    post_count = models.IntegerField(blank=True, default=0)
    topic_count = models.IntegerField(blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True)

    class Meta:
        verbose_name = _('Department Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.title

    #def save(self):
    #    pass

    @models.permalink
    def get_absolute_url(self):
        return ('erp:forum',[self.id])

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__id=self.id).select_related()

class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name='Forum')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User)
    views = models.IntegerField(blank=True, default=0)
    closed = models.BooleanField(blank=True, default=False) #Determines whethe the task is done or not
    usertags=models.ManyToManyField(User, related_name='topic_usertags', blank=True)
    iswork = models.BooleanField(default=False, verbose_name="Tick if the forum will be used to track work allotted")
    post_count = models.IntegerField(blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_topic_post', blank=True, null=True, default='')

    class Meta:
        ordering = ['-updated']
        get_latest_by = 'created'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return self.title

    @property
    def head(self):
        try:
            return self.posts.select_related().order_by('created')[0]
        except IndexError:
            return None

    @property
    def reply_count(self):
        return self.post_count - 1

    @models.permalink
    def get_absolute_url(self):
        return ('erp:topic',[self.id])

    # TODO: Defne custom methods here

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='posts', verbose_name='User')
    topic = models.ForeignKey(Topic, related_name='posts')
    updated = models.DateTimeField('Updated', blank=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name='Updated by', blank=True, null=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        return self.title

    #def save(self):
    #    pass

    #Delete post?

    @models.permalink
    def get_absolute_url(self):
        return ('erp:post',[self.id])

    def summary(self):
        LIMIT = 50
        tail = len(self.description) > LIMIT and '...' or ''
        return self.description[:LIMIT] + tail

    __unicode__ = summary    