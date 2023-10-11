from django.contrib import admin
from .models import *
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['id','user','event_name','event_date','event_time','address','city','state','pincode','description']
    
admin.site.register(Event,EventAdmin)

admin.site.register(Invitation)