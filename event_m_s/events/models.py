from django.db import models
from accounts.models import User
# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event')
    event_name = models.CharField(max_length=50)
    event_date = models.DateField()
    event_time = models.TimeField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    description = models.TextField(blank=True)
    
    
    def __str__(self):
        return self.user.get_full_name()
    
class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.user.email