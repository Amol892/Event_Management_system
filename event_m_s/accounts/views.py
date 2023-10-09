from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import detectUser
# Create your views here.



class RegisterAPI(APIView):
    
    def post(self,request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(TokenObtainPairView):
    
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            if User.objects.filter(email=email).exists():
                
                response = super().post(request)
                
                if response.status_code == status.HTTP_200_OK:
                    user = User.objects.get(email = email)
                    redirectURL = detectUser(user)
                    
                    url_data = {'redirectURL':redirectURL, 'email' : email}
                    response.data.update(url_data)
                    
                    return Response(data=response.data)
            else:
                return Response(data={'message':'Invalid email id'})
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
