from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from neo4j import GraphDatabase

from EmployersApp.models import JobAdvertisement
from EmployersApp.serializers import JobAdvertisementSerializer

from .models import ApplyRequest
from .serializers import ApplyRequestSerializer
from permissions import ApplyRequestPermission, IsJobSeeker


# Create your views here.
class FavouriteJobAdView(APIView):

    def __init__(self, **kwargs):
        self.user_id = None
        self.driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "12345678"))
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.id
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        job_id = request.data['job_id']
        with self.driver.session() as session:
            session.run(
                "MATCH (job:JobAd) WHERE job.id = $job_id MATCH (user:User) WHERE user.id = $user_id CREATE (user)-[:FAVOURITE]->(job)",
                job_id=job_id, user_id=self.user_id)
        return Response({"message": "Job added to user favourites successfully"}, status=status.HTTP_200_OK)

    def get(self, request):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (user:User) WHERE user.id = $user_id MATCH (user)-[:FAVOURITE]->(job:JobAd) RETURN job.id",
                user_id=self.user_id)
            job_ids = [record['job.id'] for record in result]
            job_ads = JobAdvertisement.objects.filter(id__in=job_ids)
        return Response(JobAdvertisementSerializer(job_ads, many=True).data, status=status.HTTP_200_OK)

    def delete(self, request):
        job_id = request.data['job_id']
        with self.driver.session() as session:
            session.run(
                "MATCH (job:JobAd) WHERE job.id = $job_id MATCH (user:User) WHERE user.id = $user_id DELETE (user)-[:FAVOURITE]->(job)",
                job_id=job_id, user_id=self.user_id)
        return Response({"message": "Job removed from user favourites successfully"}, status=status.HTTP_200_OK)


class ApplyRequestView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ApplyRequestPermission]
    queryset = ApplyRequest.objects.all()
    serializer_class = ApplyRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsJobSeeker]
        self.permission_classes = [IsAuthenticated, ApplyRequestPermission]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        apply_request = self.get_object()
        user = request.user
        if user.is_employer:
            apply_request.status = request.data['status']
            apply_request.save()
            return Response(ApplyRequestSerializer(apply_request).data, status=status.HTTP_200_OK)
        apply_request.short_description = request.data['short_description']
        apply_request.save()
        return Response(ApplyRequestSerializer(apply_request).data, status=status.HTTP_200_OK)
