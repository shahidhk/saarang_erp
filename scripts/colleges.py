from main.models import College
import xlrd
book = xlrd.open_workbook('scripts/colleges.xls')

def add_colleges():
    sheet = book.sheet_by_name('colleges')
    data = zip(sheet.col_values(1),sheet.col_values(2))
    i=0
    for college, city in data:
        try:
            College.objects.create(name=college, city=city)
            i+=1
            print i, college, city, 'Added'
        except:
            print 'error in addding ', college, i
