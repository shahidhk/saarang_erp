import xlrd
book = xlrd.open_workbook('scripts/saarang-coupons.xls')
from main.models import Coupon

def add():
    print 'Starting....'
    sheet = book.sheet_by_name('Sheet1')
    data = sheet.col_values(0)[:20000]
    i=0
    for c in data:
        i+=1
        Coupon.objects.create(code=c)
        print i, c, ' added'
    print 'Completed'