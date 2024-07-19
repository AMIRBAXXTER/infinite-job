from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'UserApp'

employer_router = DefaultRouter()
employer_router.register(r'employers', EmployerProfileView, basename='employers')

job_seeker_router = DefaultRouter()
job_seeker_router.register(r'job-seekers', JobSeekerProfileView,  basename='job-seekers')


urlpatterns = [
    path('register/', UserRegisterView.as_view(),  name='register'),
    path('login-request/', LoginCodeRequestView.as_view(),  name='login-request'),
    path('login-verify/', LoginCodeVerifyView.as_view(),  name='login-verify'),
    path('logout/', UserLogoutView.as_view(),  name='logout'),
    path('reset-password/', ResetPasswordRequestView.as_view(),  name='reset-password'),
    path('reset-password<str:uid><str:token>', ResetPasswordConfirmView.as_view(),  name='reset-password-confirm'),
    path('users/', include(employer_router.urls)),
    path('users/', include(job_seeker_router.urls)),
]
