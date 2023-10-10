from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email','mobile','gender','dob','photo','role']
        
        
    def create(self, validated_data):
            
        return User.objects.create_user(**validated_data)
    
    
# user login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
# Change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    