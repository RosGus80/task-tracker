import rest_framework.generics as generics
from rest_framework.permissions import IsAuthenticated

from tracker.models import Employee
from tracker.serializers import EmployeeSerializer


# Create your views here.


# Вьюшки модели сотрудника

class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Приписывание текущего пользователя как владельца нового экземпляра.
        Защищено от ошибки несуществования self.request.user требованием к аутентификации для доступа к вьюшке"""
        serializer.save(owner=self.request.user)


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(owner=self.request.user)

