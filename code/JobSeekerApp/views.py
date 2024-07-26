from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from neo4j import GraphDatabase

from EmployersApp.models import JobAdvertisement
from EmployersApp.serializers import JobAdvertisementSerializer

from .models import ApplyRequest
from .serializers import ApplyRequestSerializer
from permissions import ApplyRequestPermission


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


class ApplyRequestView(APIView):
    permission_classes = [IsAuthenticated, ApplyRequestPermission]

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user

    def get(self, request):
        if self.user.is_employer:
            apply_requests = ApplyRequest.objects.filter(job_advertisement__employer=request.user)
            return Response(ApplyRequestSerializer(apply_requests, many=True).data, status=status.HTTP_200_OK)
        apply_requests = ApplyRequest.objects.filter(job_seeker=request.user)
        return Response(ApplyRequestSerializer(apply_requests, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        if not self.user.is_employer:
            apply_request = ApplyRequest.objects.create(job_seeker=self.user,
                                                        job_advertisement=request.data['job_advertisement'])
            return Response(ApplyRequestSerializer(apply_request).data, status=status.HTTP_201_CREATED)
    # TODO write other methods
