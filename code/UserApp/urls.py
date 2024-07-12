from django.urls import path

from .views import *

app_name = 'UserApp'

urlpatterns = [
    path('register/', UserRegisterView.as_view(),  name='register'),
    path('login/', UserLoginView.as_view(),  name='login'),
    path('logout/', UserLogoutView.as_view(),  name='logout'),
    path('reset-password/', ResetPasswordRequestView.as_view(),  name='reset-password'),
    path('reset-password<uid:uidb64>/<token>/', ResetPasswordConfirmView.as_view(),  name='reset-password-confirm'),

]