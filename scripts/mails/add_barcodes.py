import xlrd
book = xlrd.open_workbook('scripts/barcodes_cleaned.xls')
from django.contrib.auth.models import User
from security.models import Badge

def add():
    print 'Starting....'
    sheet = book.sheet_by_name('Sheet1')
    data = zip(sheet.col_values(0),sheet.col_values(1))
    i=0
    error_list=[]
    for usr, code in data:
        i+=1
        try:
            user = User.objects.get(username=usr)
            Badge.objects.create(name=user.first_name, barcode=code)
            print i, usr, code, 'added'
        except:
            error_list.append(usr)
        print 'errors at', error_list
    print 'Completed'

    print '2nd Stage'
    sheet = book.sheet_by_name('Sheet2')
    data = zip(sheet.col_values(0),sheet.col_values(1))
    i=0
    error_list=[]
    for usr, code in data:
        i+=1
        try:
            Badge.objects.create(name=usr, barcode=code)
            print i, usr, code, 'added'
        except:
            error_list.append(usr)
        print 'errors at', error_list
    print 'Completed'