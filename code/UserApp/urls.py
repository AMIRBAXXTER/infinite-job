from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'UserApp'

router = DefaultRouter()
router.register(r'users', UserProfileView, basename='users')


urlpatterns = [
    path('register/', UserRegisterView.as_view(),  name='register'),
    path('login-request/', LoginCodeRequestView.as_view(),  name='login-request'),
    path('login-verify/', LoginCodeVerifyView.as_view(),  name='login-verify'),
    path('logout/', UserLogoutView.as_view(),  name='logout'),
    path('reset-password/', ResetPasswordRequestView.as_view(),  name='reset-password'),
    path('reset-password<str:uid><str:token>', ResetPasswordConfirmView.as_view(),  name='reset-password-confirm'),
    path('', include(router.urls)),
]