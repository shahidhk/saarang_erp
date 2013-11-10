# from django.dispatch import Signal
# from django.dispatch import receiver
# from django.core.signals import request_finished
# from django.db.models.signals import post_save 
# from forum.models import Post,Topic
# from task.models import Task
# from events.models import Event
# from notifications.models import Notification
# from userprofile.models import UserProfile,User
# from erp.models import Department
# from django.contrib.auth.models import Group

# @receiver(post_save)
# def create_callback_post(sender,**kwargs):
#     print '-------------------'
#     print sender
#     print kwargs
#     print '-------------------'
#     if kwargs['created']:
#         if sender.__name__ == 'Post':
#                 instance = kwargs['instance']
#                 body = '<span>%s</span> posted in <span>%s</span> under <span>%s</span>' %(instance.user.first_name,instance.topic.title,instance.topic.forum.title)
#                 link = '/forum/topic/%d/' %(instance.topic.id)
#                 notif = Notification(notif_body=body,link=link)
#                 notif.save()
#                 print '****************************'
#                 print instance.topic.forum.department
#                 if instance.topic.forum.department == 'public':
#                     user_list = User.objects.all()
#                 elif instance.topic.forum.department == 'coregroup':
#                     user_list = Group.objects.get(name='Core').user_set.all()
#                 else:
#                     user_list = UserProfile.objects.filter(dept=Department.objects.get(name=instance.topic.forum.department).id).user 
#                 for user in user_list:
#                     notif.receive_users.add(user)
#                 notif.save()
#                 print notif
#         elif sender.__name__ == 'Topic':
#                 instance = kwargs['instance']
#                 body = '<span>%s</span> started <span>%s</span> under <span>%s</span>' %(instance.creator.first_name,instance.title,instance.forum.title)
#                 link = '/forum/topic/%d/' %(instance.id)
#                 notif = Notification(notif_body=body,link=link)
#                 notif.save()
#                 if instance.forum.department == 'public':
#                     user_list = User.objects.all()
#                 elif instance.forum.department == 'coregroup':
#                     user_list = Group.objects.get(name='Core').user_set.all()
#                 else:
#                     user_list = UserProfile.objects.filter(dept=Department.objects.get(name=instance.topic.forum.department).id).user 
#                 for user in user_list:
#                     notif.receive_users.add(user)
#                 notif.save()
#                 print notif
#     # elif sender.__name__ == 'Task':
#     #     if kwargs[created]:
#     #         instance = kwargs['instance']
#     #         body = '<p><span>%s</span> created a <span>%s</span> task to <span>%s</span> department.</p>' %(instance.author,instance.title,instance.destin_dept.long_name)
#     #         link = 


# post_save.connect(create_callback_post)
