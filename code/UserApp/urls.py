from django.urls import path

from .views import *

app_name = 'UserApp'

urlpatterns = [
    path('index/', Index.as_view(),  name='index'),
]