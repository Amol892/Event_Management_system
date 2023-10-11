from rest_framework import serializers
from .models import *

class EventModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'
        
        
        
        
class InvitationModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Invitation
        fields ='__all__'