import random
from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .utils import detectUser
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from .models import *


# RegisterationView
class RegisterAPI(APIView):
    
    def post(self,request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View
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
                    
                    return Response(data=response.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message':'Invalid email id'})
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# User Logout View
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
    
        
# Password change View
class ChangePasswordAPI(APIView):
    
    def post(self,request,pk=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk=pk)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request,user)
                return Response(data={'message':'Your password is changed successfully'}, status=status.HTTP_200_OK)
            return Response(data={'message':'old_password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# Forgot password and OTP generation and sending to registered email
class ForgotPasswordAPI(APIView):
    
    def post(self,request):
        
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                
                user_otp, created = OTPModel.objects.get_or_create(user=user)
                user_otp.generate_otp()
                user_otp.save()
                print(user_otp.otp)
                
                # Email content
                Subject='Password reset OTP'
                message = f'Hi, {user.get_full_name()},\n Please reset your password with OTP.\nYour OTP :{user_otp.otp}'
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]
                send_mail(Subject,message,from_email,to_email)
                
        
                return Response(data={'message':'OTP is send to your email'},status=status.HTTP_200_OK)
            return Response(data={'message':'Provided email is not registered'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Reset password View
class ResetPasswordAPI(APIView):
    
    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            input_otp = serializer.validated_data['input_otp']
            reset_password = serializer.validated_data['reset_password']
            try:
                otp_obj = OTPModel.objects.get(otp=input_otp)
                user = otp_obj.user
                user.set_password(reset_password)
                user.save()
                return Response(data={'message':'New password successfully created'}, status=status.HTTP_201_CREATED)
            except OTPModel.DoesNotExist:
                return Response(data={'message':'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
                
        
            
    
    
