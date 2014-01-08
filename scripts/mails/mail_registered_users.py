from registration.models import EmailList, SaarangUser
from mailer.models import MailLog
import time, re
from django.core import mail
from django.contrib.auth.models import User

user = User.objects.get(username='ed12b031')

subject = 'Android App - Saarang 2014'
fr= 'Saarang 2014 <webadmin@saarang.org>'


SU = SaarangUser.objects.all()

SU_list=[]
for su in SU:
    try:
        if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', su.email):
            SU_list.append(su.email)
    except:
        print 'error ',su.email

tot_list = list(set(SU_list))
print len(tot_list)

html_file = open('scripts/mails/mobile_app.html', 'r')
html = html_file.read()
html_file.close()

new_mail = MailLog.objects.create(from_email='webadmin@saarang.org', 
    to_email='registered_users@saarang.org', subject=subject, 
    body=html, created_by=user)

email_list=[]
for eml in tot_list:
    msg = mail.EmailMessage(subject, html, fr, [eml])
    msg.content_subtype = "html"
    email_list.append(msg)

print 'Total ', len(email_list), ' emails has to be send.'

error_list=[]
def send_mail():
    print 'Initialising ...'
    total = len(email_list)
    start = 0
    step = 100
    j=0
    for i in range((total/step)+1):
        print 'sending....'
        try:
            connection = mail.get_connection()
            messages = email_list[start:start+step]
            for email in email_list[start:start+step]:
                j+=1
                print j,': ', email.to
            connection.send_messages(messages)
            print j, ' Emails sent. Waiting to send next batch'
        except:
            print 'error at ', j
            error_list.append(j)
        start += step
        time.sleep(2)

    print 'finished'
    print 'errors at: ', error_list
