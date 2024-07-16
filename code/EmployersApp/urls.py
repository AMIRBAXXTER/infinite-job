from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'EmployersApp'

router = DefaultRouter()
router.register(r'job_advertisements', JobAdvertisementView, basename='job_advertisements')

urlpatterns = [
    path('', include(router.urls))
    ]