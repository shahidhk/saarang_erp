# From django
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

# Model for Department forum
class Forum(models.Model):
    '''
        Defines the Forum class ie. the department Forums
    '''
    title = models.CharField(max_length=60,unique=True) # Title,
    department=models.CharField(max_length=60,choices=settings.DEPARTMENTS)
    #position = models.IntegerField('Position', blank=True, default=0) #Defines the position of the forum
    post_count = models.IntegerField(blank=True, default=0) # No of posts in the Forum
    topic_count = models.IntegerField(blank=True, default=0) # No of topics under the forum
    last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True) # Latest post

    class Meta:
        verbose_name = _('Department Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('erp:forum',[self.id])

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__id=self.id).select_related()

# Defines the Topic, which is like  a thread under each forum
class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics', verbose_name='Forum') # Key that indicates to the parent forum
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User) # Key pointing to the user who created the topic
    views = models.IntegerField(blank=True, default=0) # Counts the number of views (not implemented)
    closed = models.BooleanField(blank=True, default=False) # Determines whethe the task is done or not (not implemented)
    usertags=models.ManyToManyField(User, related_name='topic_usertags', blank=True) # points to the users tagged, that way it can be directly shown in the user homepage (not implemented yet)
    iswork = models.BooleanField(default=False, verbose_name="Work") # Check if the topic is regarding a work or not
    post_count = models.IntegerField(blank=True, default=0) # Counts the posts in the topic
    last_post = models.ForeignKey('Post', related_name='last_topic_post', blank=True, null=True, default='') # Points to the last post

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

# Defines the posts, ie replies in a topic
class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='posts', verbose_name='User') # Points to the user who created it
    topic = models.ForeignKey(Topic, related_name='posts')# Point to the parent topic
    updated = models.DateTimeField('Updated', blank=True, null=True) # Not implemented
    updated_by = models.ForeignKey(User, verbose_name='Updated by', blank=True, null=True)
    description = models.TextField(blank=True, default='') # The matter of post

    # TODO: Add options for attaching files

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

    # Returns a short summary of the post, 50 characters from description
    def summary(self):
        LIMIT = 50
        tail = len(self.description) > LIMIT and '...' or ''
        return self.description[:LIMIT] + tail

    __unicode__ = summary    