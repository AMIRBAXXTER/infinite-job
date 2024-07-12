from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from .models import CustomUser
from .tasks.send_mail import send_mail_task


# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'User already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


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
