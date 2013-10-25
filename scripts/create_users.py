from django.contrib.auth.models import User, Group, Permission
from erp.models import Department, SubDepartment
import xlrd

book = xlrd.open_workbook('scripts/erp_users.xls')

def add_dept():
    sheet = book.sheet_by_name('departments')
    # (name, long_name)
    dept = zip(sheet.col_values(1),sheet.col_values(0))
    for n, ln in dept:
        print n, ln
        obj = Department.objects.create(name=n, long_name=ln, description="Description for "+ln)
        obj.save()

def add_subdept():
    sheet = book.sheet_by_name('subdepartments  ')
    data = zip(sheet.col_values(0),sheet.col_values(2),sheet.col_values(1))
    for d, sd, lsd in data:
        print d, sd, lsd
        obj = SubDepartment.objects.create(dept=Department.objects.get(name=d), name=sd, long_name=lsd, description="Description for "+lsd)
        obj.save()

def add_cores():
    sheet = book.sheet_by_name('cores')
    # (Name, nick, dept, email, mobile, saarang email, username, pass)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5),sheet.col_values(6),sheet.col_values(7))
    for n,ni,d,e,mo,se,un,pas in data:
        core = User.objects.create_user(un, e, pas)
        core.first_name = n
        core.groups.add(Group.objects.get(name='core'))
        core.save()
        profile = core.get_profile()
        profile.status = 'core'
        profile.nick = ni
        profile.mobile = int(mo)
        profile.dept = Department.objects.get(name=d)
        profile.saarang_email = se
        profile.save()
        core.save()
        print n+" added"

def add_mobile():
    sheet = book.sheet_by_name('cores')
    # (Name, nick, dept, email, mobile, saarang email, username, pass)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5),sheet.col_values(6),sheet.col_values(7))
    for n,ni,d,e,mo,se,un,pas in data:
        core = User.objects.get(username=un)
        print core
        profile = core.get_profile()
        print mo
        print int(mo)
        profile.mobile = int(mo)
        profile.save()
        core.save()

def add_coords():
    sheet = book.sheet_by_name('Sheet7')
    # (name, roll num, email, mobile, dept, subdept)
    data = zip (sheet.col_values(0),sheet.col_values(1),sheet.col_values(2),sheet.col_values(3),sheet.col_values(4),sheet.col_values(5))
    for n,ro,e,mo,d,sd in data:
        coord = User.objects.create_user(ro, e, ro)
        coord.first_name = n
        coord.groups.add(Group.objects.get(name='coord'))
        coord.save()
        profile = coord.get_profile()
        profile.status = 'coord'
        profile.mobile = int(mo)
        profile.dept = Department.objects.get(name=d)
        profile.sub_dept = SubDepartment.objects.get(name=sd)
        profile.save()
        coord.save()
        print n+" added"
