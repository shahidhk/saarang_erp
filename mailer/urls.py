from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'mailer.views.home', name='mailer_home'),
    url(r'^massmail/$', 'mailer.views.mass_mail', name='mailer_mass_mail'),
    url(r'^massmail/send/$', 'mailer.views.send_mass_mail', name='mailer_send_mass_mail'),
    )
