from rest_framework import serializers

from .models import *
from UserApp.models import Employer


class JobAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdvertisement
        fields = [
            'title',
            'cooperation_type',
            'minimum_expertise',
            'salary',
            'description',
            'required_skills',
            'military_service_status',
            'gender',
            'employer'
        ]

    def create(self, validated_data):
        employer = Employer.objects.get(id=validated_data['employer'])

        return JobAdvertisement.objects.create(
            title=validated_data['title'],
            cooperation_type=validated_data['cooperation_type'],
            minimum_expertise=validated_data['minimum_expertise'],
            salary=validated_data['salary'],
            description=employer.description,
            required_skills=validated_data['required_skills'],
            military_service_status=validated_data['military_service_status'],
            gender=validated_data['gender'],
            employer=employer
        )
