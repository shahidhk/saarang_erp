# Create your views here.
from django.shortcuts import render
from forms import SaarangUserForm
from models import SaarangUser

def add_user(request):
    if request.method == 'POST':
        userform =SaarangUserForm(request.POST)
        if userform.is_valid():
            userform.save()
        else:
            userform = SaarangUserForm(request.POST)
    else:
        userform = SaarangUserForm()
    to_return={
            'form':userform,
            'action':  "",
            'title': "Add a new User"
        }
    return render(request, 'user_registration/new.html', to_return)

def list_users(request):
    users = SaarangUser.objects.all()
    to_return={
            'users':users,
            'action':  "",
            'title': "Registered users"
        }
    return render(request, 'user_registration/list.html', to_return)

def show_user(request, user_id):
    user = SaarangUser.objects.get(pk=user_id)
    to_return={
            'user':user,
            'action':  "",
            'title': "Registerd user details"
        }
    return render(request, 'user_registration/user.html', to_return)