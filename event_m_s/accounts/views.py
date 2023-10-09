from django.shortcuts import render
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.



class RegisterAPI(APIView):
    
    def post(self,request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


