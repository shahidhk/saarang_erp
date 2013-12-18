from registration.models import EmailList
from mailer.models import MailLog
import time
from django.core import mail
from django.contrib.auth.models import User

user = User.objects.get(username='ed12b031')

subject = 'Saarang 2014 Spotlight Events'
fr= 'webadmin@saarang.org'


EL = EmailList.objects.all()

html_file = open('scripts/mails/mass_mail.html', 'r')
html = html_file.read()
html_file.close()

new_mail = MailLog.objects.create(from_email='webadmin@saarang.org', 
    to_email='mass@saarang.org', subject=subject, 
    body=html, created_by=user)

email_list=[]
for eml in EL:
    msg = mail.EmailMessage(subject, html, fr, [eml.email])
    msg.content_subtype = "html"
    email_list.append(msg)
    print eml.email, ' parsed'

email_list = email_list[15700:]

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
                print j,': ', email
            connection.send_messages(messages)
            print j, ' Emails sent. Waiting to send next batch'
        except:
            print 'error at ', j
            error_list.append(j)
        start += step
        time.sleep(2)

    print 'finished'
    print 'errors at: ', error_list