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

@login_required(login_url='/login/')
def index(request):
    html='Hello %s , Welcome to saarang erp ' % request.user.username
    print html
    forums=Forum.objects.all()
    user=request.user
    to_return = {
            'forums': forums,
            'posts': Post.objects.count(),
            'topics': Topic.objects.count(),
            }
    return render(request, 'forum/forum.html', to_return)

@login_required(login_url='/login/')
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
    for j in topics:
        print j
 
    return render(request, 'forum/show_forum.html', to_return)

#Topic
def show_topic(request, topic_id):
    '''html='i got %d' % int(topic_id)
    return HttpResponse(html)'''
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
    to_return = {
                'topic': topic,
                'post_count': topic.post_count,
                'posts': posts,
                }
    print "ir comes after this"
    print topic.pk
    print topic.forum.pk
    return render(request, 'forum/show_topic.html', to_return)

@login_required(login_url='/login/')
def add_topic(request, forum_id):
    '''Adds a new task to the department forum'''
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.method == 'POST':
        '''
        data=request.POST.copy()    
        print data
        data['forum']=forum_id
        print data['forum']
        '''
        form=AddTopicForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.forum=forum
            data.creator=request.user
            forum.topic_count+=1
            data.save()
            forum.save()
            print data.save
            messages.success(request, 'Topic added.')
            print data.pk
            ur="/forum/%d/post/add" %data.pk
            print ur
            return redirect(ur)
        else:
            for error in form.errors:
                messages.warning(request, error)
    else:
        form=AddTopicForm()
        messages.info(request, 'Enter the fields below')
        return render(request, 'forum/add.html',{'form':form})

def add_post(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form=AddPostForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=request.user
            data.topic=topic
            data.save()
            topic.updated=datetime.datetime.now()
            topic.post_count+=1
            topic.last_post=data
            #foru is not getting updated
            topic.forum.post_count+=1
            topic.forum.last_post=data
            topic.save()
            print data.save
            messages.success(request, 'Post added.')
            print data.pk
            ur="/forum/post/%d" %data.pk
            print ur
            return redirect(ur)
        else:
            for error in form.errors:
                messages.warning(request, error)
    else:
        form=AddPostForm()
        messages.info(request, 'Enter the fields below')
    return render(request, 'forum/add.html',{'form':form})

def delete_posts(request, topic_id):
    html='i got %d' % int(topic_id)
    return HttpResponse(html)

def open_close_topic(request, topic_id, action):
    html='i got %d and %s' % (int(topic_id),str(action))
    return HttpResponse(html)

def show_post(request, post_id):
    html='i got %d' % int(post_id)
    return HttpResponse(html)

def edit_post(request, post_id):
    html='i got %d' % int(post_id)
    return HttpResponse(html)

def delete_post(request, post_id):
    html='i got %d' % int(post_id)
    return HttpResponse(html)
