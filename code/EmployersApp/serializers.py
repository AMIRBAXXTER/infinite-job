from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import *
from UserApp.models import Employer, Address


class JobAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdvertisement
        fields = '__all__'

    def create(self, validated_data):
        employer: Employer = Employer.objects.get(id=validated_data['employer'])
        content_type = ContentType.objects.get_for_model(employer)
        employer_id = employer.id
        address: Address = Address.objects.filter(content_type=content_type, object_id=employer_id)

        return JobAdvertisement.objects.create(
            title=validated_data['title'],
            location=address.province,
            cooperation_type=validated_data['cooperation_type'],
            minimum_experience=validated_data['minimum_experience'],
            salary=validated_data['salary'],
            description=employer.description,
            required_skills=validated_data['required_skills'],
            military_service_status=validated_data['military_service_status'],
            gender=validated_data['gender'],
            employer=employer
        )
