from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.permissions import has_role

from .models import User
from .serializers import EmailSerializer, TokenSerializer, UserSerializer


@api_view(["POST"])
def send_code(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        user = User(email=email)  # создаем юзера без добавления в базу
        generator = PasswordResetTokenGenerator()
        confirmation_code = generator.make_token(user)
        # сохраняем юзера в кэше на 10 минут
        cache.set(email + confirmation_code, user, 600)
        send_mail(
            'Token',
            confirmation_code,
            'from@example.com',  # Это поле От:
            [email],  # Это поле Кому:
            fail_silently=False,  # сообщать об ошибках
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        code = serializer.data['code']
        user = cache.get(email + code)
        if user is not None:
            user.username = user.email
            user.save()
            cache.delete(email + code)
            token = AccessToken.for_user(user)
            return Response(f'{token}', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (has_role('Administrator'),)
    lookup_field = "username"


class APIProfile(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
