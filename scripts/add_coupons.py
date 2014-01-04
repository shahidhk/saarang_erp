import xlrd
book = xlrd.open_workbook('scripts/saarang-coupons.xls')

def add():
    sheet = book.sheet_by_name('Sheet1')
    data = sheet.col_values(0)