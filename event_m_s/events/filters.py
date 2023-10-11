import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    #city__name = django_filters.CharFilter(field_name='city',lookup_expr='icontains')
    #event_name__name= django_filters.CharFilter(field_name='event_name',lookup_expr='icontains')
    
    class Meta:
        model = Event
        fields = {
                'event_date':['exact'],
                'city':['iexact','icontains'],
                'event_name':['iexact','icontains'],
                'user':['exact']
                  }