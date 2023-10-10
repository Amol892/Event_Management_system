from rest_framework.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('register/',RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/',LogoutAPI.as_view()),
    path('changepassword/<int:pk>/',ChangePasswordAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)