from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length=60,unique=True)
    department=models.CharField(max_length=60,choices=settings.DEPARTMENTS)

    class Meta:
        verbose_name = _('Department Forum')
        verbose_name_plural = _('Forums')

    def __unicode__(self):
        return self.title

    #def save(self):
    #    pass

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Defne custom methods here

class Topic(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    forum = models.ForeignKey(Forum)
    usertags=models.ManyToManyField(User, related_name='topic_usertags')
    iswork = models.BooleanField(default=False, verbose_name="Tick if the forum will be used to track work allotted")

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __unicode__(self):
        return self.title

    #def save(self):
    #    pass

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Defne custom methods here

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    topic = models.ForeignKey(Topic)
    body = models.TextField(max_length=10000)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __unicode__(self):
        return self.title

    #def save(self):
    #    pass

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Defne custom methods here

    