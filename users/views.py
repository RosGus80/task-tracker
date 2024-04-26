from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import SignUpSerializer, UserSerializer


# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    model = User
    serializer_class = SignUpSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Дает просматривать исключительно профиль зарегистрированного пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Дает редактировать исключительно профиль зарегистрированного пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
