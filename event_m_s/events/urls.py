from rest_framework.urls import path
from .views import *


urlpatterns = [
    path('event_invite/',InvitationEventAPIView.as_view()),
    path('event_invite/<int:pk>/',InvitationEventAPIView.as_view())
]
