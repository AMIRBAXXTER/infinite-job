from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class Index(APIView):
    def get(self):
        return Response({'message': 'Hello World'}, status=status.HTTP_200_OK)