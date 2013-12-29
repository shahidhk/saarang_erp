# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.middleware.csrf import get_token
import base64, re, os
from post_office import mail
from django.contrib import messages
from registration.models import SaarangUser
from main.forms import ProfileEditForm,CreateTeamForm,EventOptionsForm
from events.models import Event,EventRegistration,Team
from models import Feedback, College
from spons.models import SponsImageUpload
from tokens import default_token_generator as pset
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import int_to_base36, base36_to_int

def auto_id(team_id):
    base = 'SA2014'
    num = "{0:0>3}".format(team_id)
    sid = base + num
    return sid

EVENT_WITH_OPTIONS = [35,50,17,52,46,26,7,15]

def home(request):
    return HttpResponse('HOME')

def get_csrf(request):
    to_return={
    'csrf':get_token(request),
    }
    return render(request, 'main/csrf.html', to_return)

@csrf_exempt
def new_profile(request):
    filename = settings.MEDIA_ROOT+"/android.txt"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w") as text_file:
        print >>text_file, request
    data = request.POST.copy()
    try:
        user = get_object_or_404(SaarangUser, email=data['email'])
        return redirect('main_profile_edit', emailId=base64.encode(data['email']))
    except:
        new_user = SaarangUser.objects.create(email=data['email'],
        password=data['password'], name=data['name'],
        mobile=data['mobile'], gender=data['gender'], 
        college=data['college'])
        new_user.save()
        return redirect('main_profile_edit', emailId=base64.encode(data['email']))

def register_team(request,eventId,teamId):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    event = get_object_or_404(Event,id=eventId)
    team = get_object_or_404(Team,id=teamId)
    if EventRegistration.objects.filter(event=event,team=team):
        if event.id in EVENT_WITH_OPTIONS:
            return HttpResponseRedirect(reverse('band_details',kwargs={'eventId':eventId,'teamId':teamId}))
        messages.info(request,'Already registered for the event')
    else:
        if not event.registration_open :
            messages.info(request,'Registration is closed for the event.')
        else:
            EventRegistration.objects.create(participant=user,team=team,event=event,options='')
            mail_list = [member.email for member in team.members.all()]
            mail_list.append(email)
            mail.send(
                mail_list, template='email/main/register_team',
                context={'event_name':event.long_name, 'team_name':team.name,},
                )
            if event.id in EVENT_WITH_OPTIONS:
                return HttpResponseRedirect(reverse('band_details',kwargs={'eventId':eventId,'teamId':teamId}))
            messages.success(request,'Team registered successfully')
    return render(request, 'main/register_response.html')

def list_teams(request,eventId):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    to_return={}
    event = get_object_or_404(Event,id=eventId)
    team_list = []
    reg_list=[]
    try:
        team_list += list(user.team_member.all())
    except:
        pass
    try:
        team_list += list(user.team_leader.all())
    except:
        pass
    event_reg = EventRegistration.objects.filter(event=event)
    for team in team_list:
        if event_reg.filter(team=team):
            if event.id in EVENT_WITH_OPTIONS:
                reg_list+=[3]
            else:
                reg_list+=[2]
        else:
            reg_list+=[1]
    team_list = zip(team_list,reg_list)
    to_return = {
        'team_list':team_list,
        'user':user,
        'eId':event.id,
    }    
    return render(request, 'main/list_teams.html',to_return)

def register(request,eventId):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    event = get_object_or_404(Event,id=eventId)
    emailId = email
    if user.activate_status == 1:
        messages.warning(request,'Please complete your profile to register for the event. Profile can be found by clicking your email at the bottom right corner.')
        return render(request, 'main/register_response.html')
    if event.is_team:
        return HttpResponseRedirect(reverse('list_teams',kwargs={'eventId':eventId,}))#,kwargs={'eventId':eventId,'teamId':teamId,}))
    else:
        if(EventRegistration.objects.filter(participant=user,event=event)):
            messages.info(request,'Already registered for the event.')
        else:
            if not event.registration_open:
                messages.info(request,'Registration is closed for the event.')
            else:
                if user.activate_status == 2:
                    eventreg = EventRegistration()
                    eventreg.participant = user
                    eventreg.event = event
                    eventreg.options = ''
                    eventreg.save()
                    messages.success(request,'Registered successfully.')
                    mail.send(
                        [emailId], template='email/main/register_event',
                        context={'event_name':event.long_name, }
                        )
                elif user.activate_status == 1:
                    messages.warning(request,'Please complete your profile to register for the event.')
                else:
                    messages.warning(request,'Click on the activation mail sent to activate your profile.')

        return render(request, 'main/register_response.html')

def create_team(request,eventId):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    event = get_object_or_404(Event,id=eventId)
    emailId=email
    mail_list=[]
    if request.method == 'POST':
        createteamForm = CreateTeamForm(request.POST)   
        if createteamForm.is_valid():
            team_name = createteamForm.cleaned_data['team_name']
            team_members = createteamForm.cleaned_data['members']
            team = Team()
            team.name=team_name
            team.leader = user
            team.team_sid = '' 
            team.save()
            team.team_sid=auto_id(team.id)
            team.save()
            for member_email in re.findall(r'[\w\.-]+@[\w\.-]+', team_members):
                try:
                    member = SaarangUser.objects.get(email=member_email)
                    team.members.add(member)
                    mail_list.append(member_email)
                    msg = '%s has been added to the team' %(member)
                    messages.success(request,msg)
                    team.save()
                except:
                    pass            
            try:
                mail.send(
                    mail_list, template='email/main/added_to_team',
                    context={'team_name':team_name, 'user':user,}
                    )
                msg = 'Email sent to added participants'
                messages.success(request,msg)
            except:
                msg = 'Sending email failed'
                messages.error(request,msg)
            team.save()
        return HttpResponseRedirect(reverse('list_teams',kwargs={'eventId':eventId,}))#,kwargs={'eventId':eventId,'teamId':teamId,}))
    else:
        createteamForm =  CreateTeamForm()
        to_return={
            'form':createteamForm,
            'eventId':eventId,
        }
        return render(request, 'main/create_team.html',to_return)

def band_details(request,eventId,teamId):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    event = Event.objects.get(id=eventId)
    team = Team.objects.get(id=teamId)
    event_reg = EventRegistration.objects.get(event=event,team=team)
    options = event_reg.options
    print options
    try:
        options=options.split('|||')
        print options
    except:
        pass
    if request.method == 'POST':
        eventoptionsForm = EventOptionsForm(request.POST)
        if eventoptionsForm.is_valid():
            submisssion1 = eventoptionsForm.cleaned_data['submission1']
            submisssion2 = eventoptionsForm.cleaned_data['submission2']
            submisssion3 = eventoptionsForm.cleaned_data['submission3']
            band_email = eventoptionsForm.cleaned_data['band_email']
            options = 'url1===' + submisssion1 + '|||url2===' + submisssion2 + '|||url3===' + submisssion3 + '|||band_email===' + band_email 
            event_reg.options = options
            print options
            event_reg.save()
            messages.success(request,'Details saved successfully')
            return render(request, 'main/register_response.html')
    else:
        initial={}
        try:
            initial['submission1']=options[0].split('===')[1]
            print options[0].split('===')[1]
        except:
            pass
        try:
            initial['submission2']=options[1].split('===')[1]
            print options[1].split('===')[1]
        except:
            pass
        try:
            initial['submission3']=options[2].split('===')[1]
            print options[2].split('===')[1]
        except:
            pass
        try:
            initial['band_email']=options[3].split('===')[1]
            print options[3].split('===')[1]
        except:
            pass
        print initial
        eventoptionsForm = EventOptionsForm(initial=initial)
        if event.id in [35,17]:
            messages.info(request,'Please provide YouTube or Dropbox links to your <b>audio</b> submissions here.')
        else:
            messages.info(request,'Please provide YouTube or Dropbox links to your submissions here.')
        to_return = {
            'form':eventoptionsForm,
            'eventId':eventId,
        }
        return render(request, 'main/band_details.html',to_return)

######################################################################################

def login(request):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
        return render(request, 'main/logged_in.html', {'status':'logged','email':user.email,})
    except:
        colleges = College.objects.all()
        to_return = {
            'colleges':colleges,
        }
        return render(request, 'main/login.html',to_return)

def logout(request):
    try:
        del request.session['saaranguser_email']
    except KeyError:
        pass
    return render(request, 'main/logged_out.html', {})

def check_login_status(request):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
        status = 'logged'
    except:
        status='not_logged'
    return render(request, 'main/logged_in.html', {'status':status, 'email':email,})

def profile(request):
    email = request.session.get('saaranguser_email')
    try:
        user = SaarangUser.objects.get(email=email)
    except:
        messages.error(request, 'Please login to continue')
        return render(request, 'main/login.html', {})
    if request.method == 'POST':
        data = request.POST.copy()
        try:
            user.name = data['name']
            user.email = data['email']
            user.mobile = data['mobile']
            user.gender = data['gender']
            if data['college'] != 0:
                college = College.objects.get(pk=data['college'])
                user.college = college.name + ', '+ college.city
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully')
            if user.profile_is_complete():
                user.activate_status = 2
            else:
                user.activate_status = 1
            user.save()
        except:
            messages.error(request, 'Some error occured. Please try again later!')
    print user.college
    try:
        clg_name, clg_city = user.college.split(', ')
        college = College.objects.get(name=clg_name, city=clg_city).pk
    except:
        college =  user.college
    colleges = College.objects.all()
    to_return={
        'colleges':colleges,
        'user':user,
        'clg':college,
    }
    return render(request, 'main/profile.html', to_return)


def fmi(request):
    email = request.session.get('saaranguser_email')
    user = None
    try:
        user = SaarangUser.objects.get(email=email)
        if user.activate_status == 0:
            messages.error(request, 'Please click on the link sent to your email to activate your account')
        if user.activate_status == 1:
            messages.error(request, 'Please update your profile at Saarang Website to continue.')
    except:
        messages.error(request, 'Please login at Saarang Website to Submit this form')
    if user:
        if user.activate_status == 2:
            if request.method == 'POST':
                try:
                    event_regn = EventRegistration.objects.get(participant=user, event=Event.objects.get(pk=91))
                except:
                    messages.error(request, 'Please register for this event at Saarang Website and refresh this page to re-submit.')
                    return render(request, 'main/fmi_form.html', {})
                data = request.POST.copy()
                files = request.FILES
                try:
                    handle_uploaded_file(files['photo'],  'headshot', data['FirstName'])
                    handle_uploaded_file(files['photo2'], 'full_length', data['FirstName'])
                    event_regn.options = "FirstName==="+data['FirstName']+"|||LastName==="+data['LastName']+"|||age==="+data['age']+"|||college==="+data['college']+"|||address===Line:"+data['address_line_1']+",Line:"+data['address_line_2']+",Line:"+data['address_line_3']+"|||zipcode==="+data['address_zipcode']+"|||state==="+data['address_state']+"|||country==="+data['address_country']+"|||mobile==="+data['mobile']+"|||email==="+data['email']+"|||height==="+data['height']+"|||vital_stats==="+data['vital_stats']
                    event_regn.save()
                    messages.success(request, 'Registerd successfully for Femina Miss India 2014 Auditions at Saarang')
                    return render(request, 'main/register_response.html')
                except:
                    messages.error(request, 'Some error occured. Please try again later')
    to_return={}
    return render(request, 'main/fmi_form.html', to_return)

def tfi(request):
    email = request.session.get('saaranguser_email')
    user = 0
    try:
        user = SaarangUser.objects.get(email=email)
        if user.activate_status == 0:
            messages.error(request, 'Please click on the link sent to your email to activate your account')
        if user.activate_status == 1:
            messages.error(request, 'Please update your profile at Saarang Website to continue.')
    except:
        messages.error(request, 'Please login at Saarang Website to Submit this form')
    if user:
        if user.activate_status == 2:
            if request.method == 'POST':
                try:
                    event_regn = EventRegistration.objects.get(participant=user, event=Event.objects.get(pk=94))
                except:
                    messages.error(request, 'Please register for this event at Saarang Website and refresh this page to re-submit.')
                    return render(request, 'main/tfi_form.html', {'user':user,})
                data = request.POST.copy()
                try:
                    event_regn.options = "Name==="+data['FirstName']+"|||age==="+data['age']+"|||college==="+data['college']+"|||mobile==="+data['mobile']+"|||email==="+data['email']
                    event_regn.save()
                    messages.success(request, 'Registerd successfully for Education For All Run at Saarang 2014')
                    return render(request, 'main/register_response.html')
                except:
                    messages.error(request, 'Some error occured. Please try again later')
    to_return={'user':user,}
    return render(request, 'main/tfi_form.html', to_return)

def handle_uploaded_file(f, shot, name):
    filename = settings.MEDIA_ROOT +'/uploads/events/fmi/'+name+'/'+name+'_'+shot+'.jpg'
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def feedback(request):
    if request.method == 'POST':
        data = request.POST.copy()
        try:
            if data['q4'] == '5':
                string = 'other_website==' + data['other_website']
                if data['q5']:
                    string += '|||suggestion=='+data['q5']
            elif data['q4'] == '8':
                string = 'others==' + data['others']
                if data['q5']:
                    string += '|||suggestion=='+data['q5']
            else:
                string = 'suggestion=='+data['q5']
            Feedback.objects.create(q1=data['q1'], q2=data['q2'], q3=data['q3'], q4=data['q4'], suggestion=string)
            messages.success(request, 'Thank you for your feedback!')
            return render(request, 'main/register_response.html')
        except Exception, e:
            raise e
            messages.error(request, 'Some error occured. Please try again later')
    to_return={}
    return render(request, 'main/feedback.html', to_return)

def forgot_password(request):
    if request.method == 'POST':
        data = request.POST.copy()
        try:
            user = SaarangUser.objects.get(email=data['email'])
            if user.activate_status == 0:
                messages.error(request, 'Please click on the link sent to your email to activate your account')
                return render(request, 'main/password_reset_form.html', {})    
        except:
            messages.error(request, 'The email you have entered is not registered at Saarang 2014')
            return render(request, 'main/password_reset_form.html', {})
        uid = int_to_base36(user.pk)
        mail.send(
            [user.email], template='email/main/password_reset_link',
            context={'domain':'erp.saarang.org', 'uid':uid, 'token': pset.make_token(user),})
        messages.success(request, 'We have emailed you instructions for setting your password to the email address you submitted. You should be receiving it shortly.')
        return render(request, 'main/register_response.html')
    to_return = {}
    return render(request, 'main/password_reset_form.html', to_return)

def reset_password(request, uidb36, token):
    assert uidb36 is not None and token is not None
    try:
        uid_int = base36_to_int(uidb36)
        user = SaarangUser.objects.get(pk=uid_int)
    except:
        user = None

    if user is not None and pset.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            data = request.POST.copy()
            if data['new_password1'] == data['new_password2']:
                user.password = data['new_password1']
                user.save()
                messages.success(request, "Password reset successful! <a href='http://saarang.org'>Click here</a> to go to Saarang 2014")
                return render(request, 'main/register_response.html')
            else:
                messages.error(request, "Passwords does not match, please enter again")
        else:
            pass
    else:
        validlink = False
    to_return = {
        'validlink': validlink,
    }
    return render(request, 'main/password_reset_confirm.html', to_return)

def spons_page(request):
    logos = SponsImageUpload.objects.all().order_by('-priority')
    to_return={
        'logos':logos,
    }
    return render(request, 'main/spons.html', to_return)
