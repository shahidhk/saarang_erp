# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    messages.success(request, "Successfully added")

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

@login_required
def team_details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    to_return = {

       'team':team,
    }
    return render(request, 'hospi/team_details.html', to_return)

@login_required
def update_status(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    data = request.POST.copy()
    stat = ''
    try:
        stat=data['status']
    except Exception, e:
        pass
    if stat:
        print stat
        team.accomodation_status = stat
        team.save()
        messages.success(request, 'Status for '+team.name+' successfully updated to '+stat)
    return redirect('hospi_list_registered_teams')

@login_required
def statistics(request):
    teams = Team.objects.all().exclude(accomodation_status='not_req')

    pending_teams = teams.filter(accomodation_status='requested')
    confirmed_teams = teams.filter(accomodation_status='confirmed')
    waitlisted_teams = teams.filter(accomodation_status='waitlisted')
    rejected_teams = teams.filter(accomodation_status='rejected')
    
    num_pending_teams = len(pending_teams)
    num_confirmed_teams = len(confirmed_teams)
    num_waitlisted_teams = len(waitlisted_teams)
    num_rejected_teams = len(rejected_teams)

    num_total_members_pending = 0
    num_male_members_pending = 0
    num_female_members_pending = 0

    num_total_members_confirmed = 0
    num_male_members_confirmed = 0
    num_female_members_confirmed = 0

    num_total_members_waitlisted = 0
    num_male_members_waitlisted = 0
    num_female_members_waitlisted = 0

    num_total_members_rejected = 0
    num_male_members_rejected = 0
    num_female_members_rejected = 0


    for team in pending_teams:
        num_total_members_pending += team.get_total_count()
        num_male_members_pending += team.get_male_count()
        num_female_members_pending += team.get_female_count()

    for team in confirmed_teams:
        num_total_members_confirmed += team.get_total_count()
        num_male_members_confirmed += team.get_male_count()
        num_female_members_confirmed += team.get_female_count()

    for team in waitlisted_teams:
        num_total_members_waitlisted += team.get_total_count()
        num_male_members_waitlisted += team.get_male_count()
        num_female_members_waitlisted += team.get_female_count()

    for team in rejected_teams:
        num_total_members_rejected += team.get_total_count()
        num_male_members_rejected += team.get_male_count()
        num_female_members_rejected += team.get_female_count()

    num_total_members = num_total_members_pending + num_total_members_confirmed + \
        num_total_members_waitlisted + num_total_members_rejected

    num_male_members = num_male_members_pending + num_male_members_confirmed + \
        num_male_members_waitlisted + num_male_members_rejected

    num_female_members = num_female_members_pending + num_female_members_confirmed + \
        num_female_members_waitlisted + num_female_members_rejected

    num_total_teams = num_pending_teams + num_confirmed_teams + \
        num_waitlisted_teams + num_rejected_teams

    return render(request, 'hospi/statistics.html', locals())