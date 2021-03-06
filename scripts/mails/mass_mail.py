from registration.models import EmailList, SaarangUser
from mailer.models import MailLog
import time, re
from django.core import mail
from django.contrib.auth.models import User

user = User.objects.get(username='ed12b031')

subject = 'Saarang 2014 EDM Night with Sunburn Campus'
fr= 'webadmin@saarang.org'


EL = EmailList.objects.all()
SU = SaarangUser.objects.all()

SU_list=[]
for su in SU:
    try:
        if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', su.email):
            SU_list.append(su.email)
        else:
            print 'error regex mismatch ', su.email
    except:
        print 'error ',su.email

EL_list=[]
for el in  EL:
    try:
        EL_list.append(el.email)
    except:
        print 'error ', el.email

tot_list = SU_list + EL_list
print 'SU ', len(SU_list), ' EL ', len(EL_list), ' total ', len(tot_list)
duplicates_su = len(SU_list)-len(list(set(SU_list)))
duplicates_el = len(EL_list)-len(list(set(EL_list)))
print 'duplicates_el ',duplicates_el
print 'duplicates_su ',duplicates_su
tot_list = list(set(tot_list))
print len(tot_list)

html_file = open('scripts/mails/edm.html', 'r')
html = html_file.read()
html_file.close()

new_mail = MailLog.objects.create(from_email='webadmin@saarang.org', 
    to_email='mass@saarang.org', subject=subject, 
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