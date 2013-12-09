from registration.models import SaarangUser
from django.core import mail
i=1

def get_email(start, step):
    i=1
    text_file = open('scripts/email.txt', 'r')
    html_file = open('scripts/email.html', 'r')
    text = text_file.read()
    html = html_file.read()
    text_file.close()
    html_file.close()
    subject = 'Accommodation Portal open - Saarang 2014'
    fr = 'webadmin@saarang.org'
    users = SaarangUser.objects.filter(pk__range=(start,start+step))
    email_list = []
    for user in users:
        msg = mail.EmailMultiAlternatives(subject, text, fr, [user.email])
        msg.attach_alternative(html, "text/html")
        email_list.append(msg)
        print i, user.pk, user.email, ' parsed'
        i+=1
    return email_list

def send_emails(start, step):
    print 'Initialising ...'
    connection = mail.get_connection()
    messages = get_email(start, step)
    connection.send_messages(messages)
    print 'Emails sent'