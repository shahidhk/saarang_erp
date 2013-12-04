from django.db import models
from django.contrib.auth.models import User
from registration.models import SaarangUser
from events.models import Team

class Hostel(models.Model):
    name = models.CharField(max_length=50,)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=u'Type')

    def __unicode__(self):
        return (str(self.name) + ' (' + str(self.gender )+ ')')

    def get_room_count(self):
        return len(self.parent_hostel.all())

    def get_current_population(self):
        rooms = self.parent_hostel.all()
        population = 0
        for room in rooms:
            population += len(room.occupants.all())
        return population

class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Name / Number')
    hostel = models.ForeignKey(Hostel, related_name='parent_hostel')
    capacity = models.IntegerField(max_length=3)
    occupants = models.ManyToManyField(SaarangUser, related_name='room_occupant', null=True, blank=True)

    def __unicode__(self):
        return (str(self.name) + ' (' + str(self.capacity) + ' max)')

    def get_occupants_count(self):
        return len(self.occupants.all())

class Allotment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    alloted_by = models.ForeignKey(User, related_name='alloted_coord')

