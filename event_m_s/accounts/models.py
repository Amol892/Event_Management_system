from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import random
# Create your models here.



class User(AbstractUser):
    
    GENDER_CHOICES = [
        ('male','male'),
        ('female','female'),
        ('transgender','transgender')
    ]
    
    ROLE_CHOICES = [
        ('cs','customer'),
        ('ad', 'admin')
    ]
    
    
    dob = models.DateField(blank=True,default='2000-01-01')
    gender = models.CharField(max_length=11, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=50, unique=True)
    mobile = PhoneNumberField(region='IN')
    photo = models.ImageField(blank=True,upload_to='profile_photo/')
    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', 'password' )
    
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return self.first_name+" "+self.last_name
    
class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def generate_otp(self):
        self.otp = random.randint(100000,999999)
        