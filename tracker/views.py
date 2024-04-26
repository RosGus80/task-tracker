from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tracker.models import Employee, Task
from tracker.paginators import BasePaginator
from tracker.serializers import TaskCreateSerializer, EmployeeCreateSerializer, EmployeeRetrieveSerializer, \
    TaskRetrieveSerializer


# Create your views here.


# Вьюшки модели сотрудника

class EmployeeCreateAPIView(generics.CreateAPIView):
    """Эндпойнт создания сотрудника. Требует аутентификации."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Приписывание текущего пользователя как владельца нового экземпляра.
        Защищено от ошибки несуществования self.request.user требованием к аутентификации для доступа к вьюшке"""
        serializer.save(owner=self.request.user)


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпойнт просмотра сотрудника по айди, который передается в ссылке. Требует аутентификации."""
    serializer_class = EmployeeRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    """Эндпойнт редактирования сотрудника по айди, который передается в ссылке. Требует аутентификации."""
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeDestroyAPIView(generics.DestroyAPIView):
    """Эндпойнт удаления сотрудника по айди, который передается в ссылке. Требует аутентификации."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeListAPIView(generics.ListAPIView):
    """Эндпойнт для просмотра всех созданных вами сотрудников. Требует аутентификации."""
    serializer_class = EmployeeRetrieveSerializer
    pagination_class = BasePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class TaskCreateAPIView(generics.CreateAPIView):
    """Эндпойнт создания задачи. Требует аутентификации."""
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Приписывание текущего пользователя как владельца нового экземпляра.
        Защищено от ошибки несуществования self.request.user требованием к аутентификации для доступа к вьюшке"""
        serializer.save(owner=self.request.user)


class TaskRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпойнт просмотра задачи по айди, который передается в ссылке. Требует аутентификации."""
    serializer_class = TaskRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskUpdateAPIView(generics.UpdateAPIView):
    """Эндпойнт редактирования задачи по айди, который передается в ссылке. Требует аутентификации."""
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskDestroyAPIView(generics.DestroyAPIView):
    """Эндпойнт удаления задачи по айди, который передается в ссылке. Требует аутентификации."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskListAPIView(generics.ListAPIView):
    """Эндпойнт для просмотра всех созданных вами задач. Требует аутентификации."""
    serializer_class = TaskRetrieveSerializer
    pagination_class = BasePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class FreeEmployeesListAPIView(generics.ListAPIView):
    """Эндпойнт для просмотра всех ваших сотрудников, отфильтрованный по их занятости. Требует аутентификации."""
    serializer_class = EmployeeRetrieveSerializer
    pagination_class = BasePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.exclude(owner=self.request.user)