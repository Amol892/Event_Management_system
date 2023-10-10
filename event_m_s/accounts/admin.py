from django.contrib import admin
from .models import User,OTPModel
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email','password','role','is_active']
    
admin.site.register(User,UserAdmin)


admin.site.register(OTPModel)