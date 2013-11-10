# from django.dispatch import Signal
# from django.dispatch import receiver
# from django.core.signals import request_finished
# from django.db.models.signals import post_save 
# from forum.models import Post,Topic
# from task.models import Task
# from events.models import Event
# from models import Notification
# from userprofile import UserProfile
# from erp.models import Department

# @receiver(post_save)
# def create_callback_post(sender,**kwargs):
#     print sender
#     print kwargs
#     print '-------------------'
#     if sender.__name__ == 'Post':
#         print 'sdgsdg----------'
#         if kwargs['created']:
#             instance = kwargs['instance']
#             body = '<p><span>%s</span> posted in <span>%s</span> under <span>%s</span></p>' %(instance.user.first_name,instance.topic.title,instance.topic.forum.title)
#             link = '/forum/topic/%d/' %(instance.topic.id)
#             notif = Notification(notif_body=body,link=link)
#             notif.save_m2m()

#             user_list = UserProfile.objects.filter(dept=Department.objects.get(name=instance.topic.forum.department).id).user 
#             for user in user_list:
#             	notif.receive_users.add(user)
#             notif.save()
#             print notif
#     elif sender.__name__ == 'Topic':
#         print 'sgsdgsdg-----------'
#         if kwargs[created]:
#             instance = kwargs['instance']
#             body = '<p><span>%s</span> started <span>%s</span> under <span>%s</span></p>' %(instance.creator.first_name,instance.title,instance.forum.title)
#             link = '/forum/topic/%d/' %(instance.id)
#             notif = Notification(notif_body=body,link=link)
#             notif.save_m2m()

#             user_list = UserProfile.objects.filter(dept=Department.objects.get(name=instance.forum.department).id).user 
#             for user in user_list:
#                 notif.receive_users.add(user)
#             notif.save()
#             print notif
#     # elif sender.__name__ == 'Task':
#     #     if kwargs[created]:
#     #         instance = kwargs['instance']
#     #         body = '<p><span>%s</span> created a <span>%s</span> task to <span>%s</span> department.</p>' %(instance.author,instance.title,instance.destin_dept.long_name)
#     #         link = 


# post_save.connect(create_callback_post)
