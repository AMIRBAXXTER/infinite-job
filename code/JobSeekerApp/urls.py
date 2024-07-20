from django.urls import path, include

from .views import *

app_name = 'JobSeekerApp'


urlpatterns = [
    path('favourite/', FavouriteJobAdView.as_view(), name='favourite'),
]