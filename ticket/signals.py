from django.dispatch import Signal
from django.dispatch import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_save 

recieve_signal_print = Signal()

@receiver(post_save)
def signal_print(sender, **kwargs):
    if kwargs['created']:
        print 'CREATED'
    else:
        print 'EDITED'

post_save.connect(signal_print)