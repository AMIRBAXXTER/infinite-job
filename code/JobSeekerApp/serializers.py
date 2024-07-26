from rest_framework.serializers import ModelSerializer

from JobSeekerApp.models import ApplyRequest


class ApplyRequestSerializer(ModelSerializer):

    class Meta:
        model = ApplyRequest
        fields = '__all__'

