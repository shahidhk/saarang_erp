from erp.models import Department,SubDepartment
from events.models import Event
from userprofile.models import User

def split_select(input_array):
    out_dept=[]
    out_subdept=[]
    out_event=[]
    out_user=[]
    for item in input_array:
        a = item[0]
        if a == 'd':
            out_dept.append(Department.objects.get(id=int(item[1:])))
        if a == 's':
            out_subdept.append(SubDepartment.objects.get(id=int(item[1:])))
        if a == 'e':
            out_event.append(Event.objects.get(id=int(item[1:])))
        if a == 'u':
            out_user.append(User.objects.get(id=int(item[1:])))
    return out_dept,out_subdept,out_event,out_user
    