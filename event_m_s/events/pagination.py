from rest_framework.pagination import PageNumberPagination, CursorPagination

class MyPagination(CursorPagination):
    ordering = 'event_date'
    page_size = 5