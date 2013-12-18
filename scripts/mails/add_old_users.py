import xlrd
from registration.models import EmailList
import re

book = xlrd.open_workbook('scripts/mails/last_year_users.xls')
sheet = book.sheet_by_name('Sheet1')
data=sheet.col_values(0)

print len(data)
print type(data)

sheet2 = book.sheet_by_name('Sheet2')
data2=sheet2.col_values(0)

print len(data2)
print type(data2)


print 'removing duplicates'

data = list(set(data))
data2=list(set(data2))

final=data+data2

final = list(set(final))
invalid_list=[]
i=0
j=0
for email in final:
    email=email.lower()
    try:
        if re.match(r'[^@]+@[^@]+\.[^@]+', email):
            EmailList.objects.create(email=email)
            print i, email, 'added'
            i+=1
    except:
        invalid_list.append(email)
        j+=1


print i, ' emails added to database'
print j, ' failed'

print invalid_list

print len(final)