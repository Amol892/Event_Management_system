from rest_framework.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('register/',RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('changepassword/<int:pk>/',ChangePasswordAPIView.as_view()),
    path('forgotpassword/',ForgotPasswordAPIView.as_view()),
    path('resetpassword/',ResetPasswordAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)