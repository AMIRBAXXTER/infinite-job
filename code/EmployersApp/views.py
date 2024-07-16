from .models import JobAdvertisement
from .serializers import JobAdvertisementSerializer
from rest_framework import viewsets


# Create your views here.


class JobAdvertisementView(viewsets.ModelViewSet):
    queryset = JobAdvertisement.objects.all()
    serializer_class = JobAdvertisementSerializer

