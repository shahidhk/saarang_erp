# From Django
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^create_ticket/$', 'ticket.views.create_ticket', name='create_ticket'),
    url(r'^ticket_list/$', 'ticket.views.ticket_list', name='ticket_list'),
    url(r'^edit_ticket/(?P<ticket_id>\d+)/$', 'ticket.views.edit_ticket', name='edit_ticket'),
    url(r'^delete_ticket/(?P<ticket_id>\d+)/$', 'ticket.views.delete_ticket', name='delete_ticket'),
    url(r'^new_transaction/$', 'ticket.views.new_transaction', name='new_transaction'),
    url(r'^transaction_list/$', 'ticket.views.transaction_list', name='transaction_list'),
    url(r'^statistics/$', 'ticket.views.statistics', name='statistics'),
)