import django_filters.rest_framework as filters
from .models import JobAdvertisement


class JobAdvertisementFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name='salary', lookup_expr='lte')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = JobAdvertisement
        fields = ['minimum_experience', 'military_service_status', 'gender']
