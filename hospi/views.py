# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from registration.models import SaarangUser
from models import Hostel, Room
from events.models import Team, EventRegistration, Event
from forms import HostelForm, RoomForm
from events.forms import AddTeamForm

####################################################################
# Mainsite Views
def home(request):
    if not request.session.get('saaranguser_email'):
        return redirect('hospi_login')
    email = request.session.get('saaranguser_email')
    user = SaarangUser.objects.get(email=email)
    teams_leading = user.team_leader.all()
    if len(user.team_leader.all()) != 0:
        team = teams_leading[0]
    else:
        messages.error(request, 'You do not lead any team. Please create a team')
        return redirect('hospi_login')
    members = teams_leading[0].members.all()
    edits = ['not_req', 'requested']
    if team.accomodation_status in edits:
        editable = True
    else:
        editable = False
    to_return = {
        'editable':editable,
        'leader':user,
        'team':team,
        'members':members,
    }
    return render(request, 'hospi/home.html', to_return)

def login(request):
    if request.method == 'POST':
        data=request.POST.copy()
        try:
            user = SaarangUser.objects.get(email=data['email'])
            try:
                teams = user.team_leader.all()
            except Exception, e:
                messages.error(request, 'You do not lead any team. Please create a team')
                return render(request, 'hospi/login.html')
            if user.password == data['password']:
                request.session['saaranguser_email'] = user.email
                return redirect('hospi_home')
            else:
                messages.error(request, 'Did u mis-spell your password?')
        except Exception, e:
            messages.error(request, 'Is your email id correct?')
    return render(request, 'hospi/login.html')

def logout(request):
    try:
        del request.session['saaranguser_email']
        messages.success(request, 'You have been logged out')
    except KeyError:
        messages.warning(request, 'Please login first')
    return redirect('hospi_login')


def add_members(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])
    return_list = zip(dict(request.POST)['email'],dict(request.POST)['college_id'])
    not_registered =[]
    for member in return_list:
        uemail = member[0]
        uid = member[1]
        try:
            user = SaarangUser.objects.get(email=uemail)
            if uid:
                user.college_id = uid
                user.save()
            new = team.members.add(user)
        except Exception, e:
            not_registered.append(uemail)
    if not not_registered:
        messages.success(request, "Successfully added")
    elif not_registered:
        msg=''
        for email in not_registered:
            msg += email + ', '
        messages.error(request,'Partially added members. ' + msg + 'have not registered \
                with Saarang yet. Please ask them to register and try adding them again.')
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
        messages.success(request, 'Successfully requested for accommodation.')
    else:
        messages.success(request, 'Details successfully updated.')
    team.save()
    return redirect('hospi_home')

def generate_saar(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    leader = team.leader
    members = team.members.all()
    to_return = {
        'leader':leader,
        'team':team,
        'members':members,
    }
    return render(request, 'hospi/saar.html', to_return)

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
    edit_list = ['confirmed', 'rejected']
    if team.accomodation_status in edit_list:
        editable = False
    else:
        editable=True
    to_return = {
        'editable':editable,
        'team':team,
    }
    return render(request, 'hospi/team_details.html', to_return)

@login_required
def update_status(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
        messages.warning(request, 'For '+ team.name + ' : ' + team.team_sid +', Team leader found in members list also. Successfully removed!')
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

#####################################################################################

# Hospi Control room
@login_required
def add_hostel_rooms(request):
    hostelform = HostelForm()
    roomform = RoomForm()
    to_return = {
        'hostelform':hostelform,
        'roomform':roomform,
    }
    return render(request, 'hospi/add_hostel_rooms.html', to_return)

@login_required
def add_hostel(request):
    try:
        hostel = HostelForm(request.POST)
        hos = hostel.save()
        messages.success(request, 'Hostel ' + hos.name + ' successfully added')
    except Exception, e:
        messages.error(request, 'Some error occured. Please contact webops with this message: '+ e.message)
    return redirect('hospi_room_map')

@login_required
def add_room(request):
    try:
        room = RoomForm(request.POST)
        rom = room.save()
        messages.success(request, 'Room ' + rom.name + ' successfully added')
    except Exception, e:
        messages.error(request, 'Some error occured. Please contact webops with this message: '+ e.message)
    return redirect('hospi_room_map')

@login_required
def room_map(request):
    hostels = Hostel.objects.all()
    to_return = {
        'hostels':hostels,
    }
    return render(request, 'hospi/room_map.html', to_return)

@login_required
def hostel_details(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    rooms = hostel.parent_hostel.all()
    to_return={
        'hostel':hostel,
        'rooms':rooms,
    }
    return render(request, 'hospi/hostel_details.html', to_return)

@login_required
def room_details(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    to_return={
        'room':room,
    }
    return render(request, 'hospi/room_details.html', to_return)

@login_required
def list_all_teams(request):
    teams = Team.objects.all()
    to_return={
        'teams':teams,
    }
    return render(request, 'hospi/list_all_teams.html', to_return)    

def auto_id(team_id):
    base = 'SA2014'
    num = "{0:0>3d}".format(team_id)
    sid = base + num
    return sid

@login_required
def add_team(request):
    addteamForm = AddTeamForm()
    events = Event.objects.filter(is_team=True)
    to_return={
        'events':events,
        'form': addteamForm,
        }
    return render(request, 'hospi/add_team.html', to_return)

@login_required
def save_team(request):
    addteamForm = AddTeamForm(request.POST)
    data = request.POST.copy()
    if addteamForm.is_valid():
        try:
            team = addteamForm.save()
            team.team_sid = auto_id(team.pk)
            event = Event.objects.get(pk=data['event_id'])
            print 'OK'
            event_regn = EventRegistration.objects.create(participant=team.leader, \
             event=event, team=team)
            event_regn.save()
            team.save()
            messages.success(request, team.name +' added successfully. Saarang ID is '+team.team_sid)
        except Exception, e:
            messages.error(request, 'Some error occured. please try again: ' + e.message)
    else:
        messages.error(request, 'Some error occured. please try again')
    return redirect('hospi_list_registered_teams')

@login_required
def check_in_team(request, team_id):
    '''Needs to add some validators'''
    team = get_object_or_404(Team, pk=team_id)
    if team.get_male_count() == 0 and team.get_female_count==0:
        messages.error(request, 'Incomplete team profile')
    if team.members.filter(email=team.leader.email):
        team.members.remove(team.leader)
    if team.get_female_count() and team.get_male_count():
        print 'Mixed Team'
        males = team.get_male_members()
        females = team.get_female_members()
        male_rooms = Room.objects.filter(hostel__gender='male')
        female_rooms = Room.objects.filter(hostel__gender='female')
        return render(request, 'hospi/check_in_mixed.html', locals())
    elif team.get_male_count():
        print 'Male Team'
        males = team.get_male_members()
        male_rooms = Room.objects.filter(hostel__gender='male')
        return render(request, 'hospi/check_in_males.html', locals())
    elif team.get_female_count():
        print 'Female Team'
        females = team.get_female_members()
        female_rooms = Room.objects.filter(hostel__gender='female')
        return render(request, 'hospi/check_in_females.html', locals())
    return HttpResponse("<div class='alert alert-error'> Incomplete team profile</div>")

@login_required
def check_in_mixed(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])
    males = team.get_male_members()
    females = team.get_female_members()
    for male in males:
        room = get_object_or_404(Room, pk=data[male.saarang_id])
        room.occupants.add(male)
        room.save()
    for female in females:
        room = get_object_or_404(Room, pk=data[female.saarang_id])
        room.occupants.add(female)
        room.save()
    team.checked_status = 'in'
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def check_in_males(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])
    males = team.get_male_members()
    for male in males:
        room = get_object_or_404(Room, pk=data[male.saarang_id])
        room.occupants.add(male)
        room.save()
    team.checked_status = 'in'
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def check_in_females(request):
    data = request.POST.copy()
    team = get_object_or_404(Team, pk=data['team_id'])
    females = team.get_female_members()
    for female in females:
        room = get_object_or_404(Room, pk=data[female.saarang_id])
        room.occupants.add(female)
        room.save()
    team.checked_status = 'in'
    team.save()
    messages.success(request, team.team_sid + ' checked in successfully')
    return redirect('hospi_list_registered_teams')

@login_required
def check_out_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.members.all()
    for member in members:
        room = member.room_occupant.all()[0]
        room.occupants.remove(member)
        room.save()
    team.checked_status = 'out'
    team.save()
    messages.success(request, team.team_sid + ' checked out successfully')
    return redirect('hospi_list_registered_teams')
