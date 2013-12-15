import time
from django.core import mail

from hospi.models import HospiTeam as ht

from registration.models import SaarangUser as su


subject = 'Profile not complete - Accommodation Portal - Saarang 2014'
fr = 'webadmin@saarang.org'
members_text ="As the team leader, it is your responsibility to ensure that all of your team member's profiles are complete. We have noticed that the below listed members' profiles are incomplete. Please inform them to update them as soon as possible.<br/>"

teams = ht.objects.all()

email_list=[]
for team in teams:
    incomplete=[]
    leader_incomplete = False
    members_text ="As the team leader, it is your responsibility to ensure that all of your team member's profiles are complete. We have noticed that the below listed members' profiles are incomplete. Please inform them to update them as soon as possible.<br/>"
    print '--------------------------------------------------'
    print team.name
    members=team.get_all_members()
    members.remove(team.leader)
    if not team.leader.profile_is_complete():
        leader_incomplete = True
        print 'Leader profile incomplete'
        print team.leader.name
        print team.leader.gender
        print team.leader.email
        print team.leader.mobile
        print team.leader.college
        print '====='
    for member in members:
        if not member.profile_is_complete():
            print 'member profile incomplete'
            print member.name
            print member.gender
            print member.email
            print member.mobile
            print member.college
            print '====='
            incomplete.append(member.email)
            members_text += "<li>"+member.email+"</li>"
    if leader_incomplete and incomplete and team.accomodation_status == 'requested':
        leader_body='<p>Hello, </p><p>Greetings from Saarang 2014.</p><p>We are happy to see that you have registered team: %s for accommodation at Saarang. But, we have found out that your profile at Saarang website is not complete. Please click <a href="http://saarang.org/2014/main/#login" target="_blank">here</a> and update your profile as soon as possible, to help us serve you better.</p><p><strong>Please note that it is necessary to complete your profile to be eligible for accommodation.</strong></p><p>%s</p><p>You can update your profile by clicking on your email at the bottom right corner of the Saarang Website if you are already logged in.</p><p>P.S - Kindly note that your registration alone does not guarantee your accomodation. All further details will be conveyed to you by mail after your request has been confirmed.</p><p>Wishing you a happy Saarang,</p><p>Web Operations Team,<br/>Saarang 2014</p>'%(team.name, members_text)
        msg = mail.EmailMessage(subject, leader_body, fr, [team.leader.email])
        msg.content_subtype = "html"
        email_list.append(msg)
        print team.pk, team.name, ' parsed'
    elif not leader_incomplete and incomplete and team.accomodation_status == 'requested':
        no_leader_body ="<p>Hello, </p><p>Greetings from Saarang 2014.</p><p>We are happy to see that you have registered team: %s for accommodation at Saarang. But, we have found out that your team members' profile at Saarang website is not complete.</p><p><strong>Please note that it is necessary to complete the profile to be eligible for accommodation.</strong></p><p>%s</p><p>P.S - Kindly note that your registration alone doesn't guarantee your accomodation. All further details will be conveyed to you by mail after your request has been confirmed.</p><p>Wishing you a happy Saarang,</p><p>Web Operations Team,<br/>Saarang 2014</p>"%(team.name, members_text)
        msg = mail.EmailMessage(subject, no_leader_body, fr, [team.leader.email])
        msg.content_subtype = "html"
        email_list.append(msg)
        print team.pk, team.name, ' parsed'


print 'Total ', len(email_list), ' emails has to be send.'

def send_mail():
    print 'Initialising ...'
    total = len(email_list)
    start = 0
    step = 50
    j=0
    for i in range((total/50)+1):
        print 'sending....'
        connection = mail.get_connection()
        messages = email_list[start:start+step]
        for email in email_list[start:start+step]:
            j+=1
            print j,': ', email
        connection.send_messages(messages)
        print j, ' Emails sent. Waiting to send next batch'
        start += step
        time.sleep(10)

    print 'finished'

