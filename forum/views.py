from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib import messages
from forum.models import Forum, Topic, Post
from django.db.models import Q, F
import datetime
from forum.forms import AddTopicForm, AddPostForm
from userprofile.models import UserProfile
from userprofile.forms import UserProfileForm
from notifications.models import Notification
from erp.models import Department

@login_required
def index(request):
    html='Hello %s , Welcome to the Saarang ERP ' % request.user.username
    print html
    forums=Forum.objects.all()
    user=request.user
    to_return = {
            'forums': forums,
            'posts': Post.objects.count(),
            'topics': Topic.objects.count(),
            }
    return render(request, 'forum/forum.html', to_return)

@login_required
def show_forum(request, forum_id):
    '''
    html='i got %d' % int(forum_id)
    return HttpResponse(html)'''
    forum = get_object_or_404(Forum, pk=forum_id)
    #if not forum.category.has_access(request.user):
        #   return HttpResponseForbidden()
    topics = forum.topics.order_by('-updated').select_related()
    to_return = {
                'forum': forum,
                'posts': forum.post_count,
                'topics': topics,
                }   
    #for j in topics:
        #print j
 
    return render(request, 'forum/show_forum.html', to_return)

#Topic
@login_required
def show_topic(request, topic_id):
    '''html='i got %d' % int(topic_id) return HttpResponse(html)'''
    post_request = request.method == "POST"
    user_is_authenticated = request.user.is_authenticated()
    if post_request and not user_is_authenticated:
        # Info: only user that are logged in should get forms in the page.
        return HttpResponseForbidden()

    topic = get_object_or_404(Topic.objects.select_related(), pk=topic_id)
    Topic.objects.filter(pk=topic.id).update(views=F('views') + 1)

    last_post = topic.last_post

    #if request.user.is_authenticated():
    #    topic.update_read(request.user)
    posts = topic.posts.all().select_related()
    #for i in posts:
        ## This will truncates the description if it is greater than 100 characters and adds some dots
        #i.description = (i.description[:300] + " ....") if len(i.description) > 300 else i.description
        ##i.description = i.description
    to_return = {
                'topic': topic,
                'post_count': topic.post_count,
                'posts': posts,
                }
    return render(request, 'forum/show_topic.html', to_return)

@login_required
def add_topic(request, forum_id):
    '''Adds a new task to the department forum'''
    forum = get_object_or_404(Forum, pk=forum_id)
    topics = forum.topics.order_by('-updated').select_related()
       
    if request.method == 'POST':
        form=AddTopicForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.forum=forum
            data.creator=request.user
            forum.topic_count+=1
            data.save()
            body = '<span style="color:blue;">%s</span> started <span style="color:red;">%s</span> under <span style="color:green;">%s</span>' %(request.user.first_name,data.title,data.forum.title)
            link = '/forum/topic/%d/' %(data.id)
            notif = Notification(notif_body=body,link=link)
            notif.save()
            if data.forum.department == 'public':
                notif.is_public = True
            elif data.forum.department == 'coregroup':
                for user in Group.objects.get(name='Core').user_set.all():
                    notif.receive_users.add(user)
            else:
                notif.depts.add(Department.objects.get(name=data.forum.department))
            notif.save()
            print notif.depts.all()
            forum.save()
            return redirect('forum.views.add_post',topic_id=data.pk)
        else:
            for error in form.errors:
                pass
    else:
        form=AddTopicForm()
    return render(request, 'forum/add_topic.html',{'form':form, 'forum': forum, 'topics': topics, })

@login_required
def add_post(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    profile = get_object_or_404(UserProfile, pk=request.user.id)
    posts = topic.posts.all().select_related()
    #for i in posts:
        # This will truncates the description if it is greater than 100 characters and adds some dots
        #i.description = (i.description[:300] + " ....") if len(i.description) > 300 else i.description
        #i.description = i.description
    if request.method == 'POST':
        form=AddPostForm(request.POST)
        if form.is_valid():
            profile.post_count+=1
            profile.save()
            data=form.save(commit=False)
            data.user=request.user
            data.topic=topic
            data.save()
            body = '<span style="color:blue;">%s</span> posted in <span style="color:red;">%s</span> under <span style="color:green;">%s</span>' %(request.user.first_name,data.topic.title,data.topic.forum.title)
            link = '/forum/topic/%d/' %(data.topic.id)
            notif = Notification(notif_body=body,link=link)
            notif.save()
            if data.topic.forum.department == 'public':
                notif.is_public = True
            elif data.topic.forum.department == 'coregroup':
                print '-------------------'
                print 'coregroup'
                print '-------------------'
                for user in Group.objects.get(name='Core').user_set.all():
                    notif.receive_users.add(user)
            else:
                notif.receive_depts.add(Department.objects.get(name=data.topic.forum.department))
            notif.save()
            print notif.receive_depts.all()
            topic.updated=datetime.datetime.now()
            topic.post_count+=1
            topic.last_post=data
            topic.save()
            print topic.forum.pk
            forum = get_object_or_404(Forum, pk=topic.forum.pk)
            print forum
            forum.post_count+=1
            forum.last_post=data
            forum.save()
            print data.pk
            return redirect('forum.views.show_topic', topic_id = topic.pk)
        else:
            for error in form.errors:
                messages.warning(request, error)
    else:
        form=AddPostForm()
    return render(request, 'forum/add.html',{ 'form':form, 'topic': topic, 'post_count': topic.post_count, 'posts': posts, })

@login_required 
def delete_posts(request, topic_id):
    html='i got %d' % int(topic_id)
    return HttpResponse(html)

@login_required
def open_close_topic(request, topic_id, action):
    html='i got %d and %s' % (int(topic_id),str(action))
    return HttpResponse(html)

@login_required
def show_post(request, post_id):
    post= get_object_or_404(Post, pk=post_id)
    return render(request, 'forum/show_post.html',{'post':post})

@login_required
def edit_post(request, post_id):
    html='i got %d' % int(post_id)
    return HttpResponse(html)

@login_required
def delete_post(request, post_id):
    html='i got %d' % int(post_id)
    return HttpResponse(html)
