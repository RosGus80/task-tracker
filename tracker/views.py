from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tracker.models import Employee, Task
from tracker.serializers import TaskCreateSerializer, EmployeeCreateSerializer, EmployeeRetrieveSerializer, \
    TaskRetrieveSerializer


# Create your views here.


# Вьюшки модели сотрудника

class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Приписывание текущего пользователя как владельца нового экземпляра.
        Защищено от ошибки несуществования self.request.user требованием к аутентификации для доступа к вьюшке"""
        serializer.save(owner=self.request.user)


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Приписывание текущего пользователя как владельца нового экземпляра.
        Защищено от ошибки несуществования self.request.user требованием к аутентификации для доступа к вьюшке"""
        serializer.save(owner=self.request.user)


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TaskRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
