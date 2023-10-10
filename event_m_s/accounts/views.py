from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .utils import detectUser
from django.contrib.auth import update_session_auth_hash
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
        
        
class LogoutAPI(APIView):
    
    def post(sef,request):
        print(request.data)
        try:
            refresh_token = request.data['refresh']  # refresh is used as key for refresh token, which is included in request body.
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            
            return Response(data = {'message':'your account is successfully logouted'},status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(data={'message':'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
    
        

class ChangePasswordAPI(APIView):
    
    def post(self,request,pk=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk=pk)
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request,user)
                return Response(data={'message':'Your password is changed successfully'}, status=status.HTTP_200_OK)
            return Response(data={'message':'old_password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)