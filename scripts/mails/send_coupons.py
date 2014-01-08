 
from registration.models import EmailList, SaarangUser
from mailer.models import MailLog
import time, re
from django.core import mail
from django.template.loader import render_to_string
from main.models import Coupon, LastCoupon
from django.shortcuts import get_object_or_404

user = User.objects.get(username='ed12b031')

subject = 'Saarang 2014 Goodies - Free Recharge Coupons'
fr= 'Saarang 2014 <webadmin@saarang.org>'


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

tot_list = SU_list 
print 'SU ', len(SU_list), ' total ', len(tot_list)
duplicates_su = len(SU_list)-len(list(set(SU_list)))
print 'duplicates_su ',duplicates_su
tot_list = list(set(tot_list))
print len(tot_list)

rendered = render_to_string('email_coupon.html', {'foo': 'bar'})
coupon_code_link = 'https://www.komparify.com/recharge?couponcode='+coupon.code

email_list=[]
for eml in tot_list:
    last = get_object_or_404(LastCoupon, pk=1)
    last_coupon = int(last.coupon_id)
    coupon = get_object_or_404(Coupon, pk=last_coupon, sent=False)
    rendered = render_to_string('email_coupon.html', {'coupon_code_link': 'https://www.komparify.com/recharge?couponcode='+coupon.code})
    msg = mail.EmailMessage(subject, rendered, fr, [eml])
    msg.content_subtype = "html"
    email_list.append(msg)
    coupon.sent = True
    coupon.sent_to = user
    coupon.save()
    last.coupon_id += 1
    last.save()

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