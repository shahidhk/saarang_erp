from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'mailer.views.home', name='mailer_home'),
    )
