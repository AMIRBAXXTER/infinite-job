from random import randint

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import CustomUser
from .tasks.send_mail import send_mail_task
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse


# Create your views here.

@extend_schema(
    parameters=[UserRegisterSerializer],
)
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class LoginCodeRequestView(APIView):

    @extend_schema(
        parameters=[LoginCodeRequestSerializer],
        request=LoginCodeRequestSerializer,
    )
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'User already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginCodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            login_code = randint(1000, 9999)
            cache_key = f'login_code_{email}'
            cache.set(cache_key, login_code, timeout=60)
            massage = f'Your login code is {login_code}'
            send_mail_task.apply_async(args=['login code', massage, [email]])
            return Response({'message': 'Login code sent to email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginCodeVerifyView(APIView):
    def post(self, request):
        serializer = LoginCodeVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.filter(email=serializer.data.get('email')).first()

            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class ResetPasswordRequestView(APIView):

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'error': 'Please provide email'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'http://0.0.0.0:8000/reset-password?uid={uid}&token={token}'
        send_mail_task.apply_async(args=['reset password', reset_link, [email]])
        return Response({'message': 'Reset link sent to your email'}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(APIView):
    def post(self, request, uid=None, token=None):
        if token is None or uid is None:
            return Response({'error': 'Please provide token and uid'}, status=status.HTTP_400_BAD_REQUEST)
        uid = urlsafe_base64_decode(uid).decode()
        user = CustomUser.objects.filter(pk=uid).first()
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid Token'}, status=status.HTTP_404_NOT_FOUND)
        password = request.data.get('password')
        if password is None:
            return Response({'error': 'Please provide password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class UserProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_employer:
            return EmployerProfileSerializer
        return JobSeekerProfileSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'massage': 'User Profile can not be deleted'}, status=status.HTTP_400_BAD_REQUEST)
