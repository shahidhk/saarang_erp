# Create your views here.
from models import Notification

def list_notifications(request):
    notif_list = Notification.objects.all()
    return render(request, 'home.html', locals())
