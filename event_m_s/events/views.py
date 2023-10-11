from django.shortcuts import get_object_or_404, render
from .serializers import *
from rest_framework import mixins, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .filters import EventFilter
from .models import Event
from rest_framework.views import APIView
from .pagination import MyPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


   
# Events list with pagination, sorting by event date, and Date filter, Searching by Event name and city
class EventListViewsetAPI(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    

    #Pagination 
    pagination_class = MyPagination

    # Sorting and filtering
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = EventFilter
    filterset_fields = ['event_date','city','event_name','user']
    
    ordering_fields = ('event_date',) # Sorting by event_date
    ordering = ('event_date',) # Default sorting order

    

# API for Event model manipulation operations
class EventViewSetAPI(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    
    
    def update(self, request,pk=None):
        instance=self.get_object()
        print(type(request.data['user']))
        print(type(instance.user.id))
        if instance.user.id == int(request.data['user']):
            serializer = EventModelSerializer(data=request.data,instance=instance)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data,status=status.HTTP_205_RESET_CONTENT)
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'message':'you does not have permission to update this event'},status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self,request,pk=None):
        instance = self.get_object()
        print(request.user)
        print(instance.user)
        if instance.user == request.user:
            instance.delete()
            return Response(data={'message':'Event record is deleted'},status=status.HTTP_204_NO_CONTENT)
        return Response(data={'message':'you does not have permission to delete this event'},status=status.HTTP_403_FORBIDDEN)
        
        
        
    
