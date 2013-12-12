from django.core import mail

from hospi.models import HospiTeam as ht

from registration.models import SaarangUser as su

teams = ht.objects.all()

incomplete=[]

for team in teams:
    members=team.get_all_members()
    for member in members:
        if not member.profile_is_complete():
            incomplete.append(member.email)

text_file = open('scripts/email_profile.txt', 'r')
html_file = open('scripts/email_profile.html', 'r')
text = text_file.read()
html = html_file.read()
text_file.close()
html_file.close()
subject = 'Profile not completed - Accommodation Portal - Saarang 2014'
fr = 'webadmin@saarang.org'

incomplete = list(set(incomplete))

email_list=[]
for user in incomplete:
    msg = mail.EmailMultiAlternatives(subject, text, fr, [user])
    msg.attach_alternative(html, "text/html")
    email_list.append(msg)
    print user, ' parsed'
print 'Total ', len(email_list), ' emails has to be send.'

def send_mail(start, step):
    print 'Initialising ...'
    connection = mail.get_connection()
    messages = email_list[start:start+step]
    connection.send_messages(messages)
    print 'Emails sent' 