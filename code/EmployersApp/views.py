from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .filters import JobAdvertisementFilter
from .models import JobAdvertisement
from .serializers import JobAdvertisementSerializer
from rest_framework import viewsets

# Create your views here.


class JobAdvertisementView(viewsets.ModelViewSet):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobAdvertisementFilter
    search_fields = ['title', 'description']