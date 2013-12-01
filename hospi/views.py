# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from registration.models import SaarangUser
from models import Team

####################################################################
# Mainsite Views
def home(request):
    email = 'muhammedshahid.k@gmail.com'
    user = SaarangUser.objects.get(email=email)
    teams_leading = user.team_leader.all()
    team = teams_leading[0]
    members = teams_leading[0].members.all()

    print user
    print teams_leading
    print members
    to_return = {
        'leader':user,
        'team':team,
        'members':members,
    }
    return render(request, 'hospi/home.html', to_return)

def add_members(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])
    return_list = zip(dict(request.POST)['email'],dict(request.POST)['college_id'])
    for member in return_list:
        uemail = member[0]
        uid = member[1]
        user = get_object_or_404(SaarangUser, email=uemail)
        new =  team.members.add(user)

    print Team.get_total_count(team)
    return redirect('hospi_home')

def delete_member(request, team_id, member_id):
    team = get_object_or_404(Team, pk=team_id)
    user = get_object_or_404(SaarangUser, pk=member_id)

    team.members.remove(user)
    return redirect('hospi_home')

def add_accomodation(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])

    team.date_of_arrival = data['arr_date']
    team.date_of_departure = data['dep_date']
    team.time_of_arrival = data['arr_time']
    team.time_of_departure = data['dep_time']
    if team.accomodation_status == 'not_req':
        team.accomodation_status = 'requested'
    team.save()
    return redirect('hospi_home')

# End Mainsite views
#######################################################################

# ERP views

@login_required
def list_registered_teams(request):
    teams = Team.objects.all().exclude(accomodation_status='not_req')
    to_return = {
       'teams':teams,
    }
    return render(request, 'hospi/registered_teams.html', to_return)