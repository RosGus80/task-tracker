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
    """Эндпойнт для просмотра всех ваших сотрудников, отфильтрованный по их занятости (наиболее свободные впереди).
    Требует аутентификации."""
    serializer_class = EmployeeRetrieveSerializer
    pagination_class = BasePaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает список сотрудников авторизованного пользователя, сортируя по количеству приписанных к ним задач
        и выводя самых менее нагруженных вперед"""

        """К сожалению, я не смог встроенными средствами джанго реализовать фильтрацию. Моя лучшая попытка - 
        закомментированный ниже код. Оставил его на случай, если смогу доработать. Его проблема заключается в том, что
        он считает все задачи, приписанные работнику, но он не должен считать выполненные задачи, но отфильтровать
        выполненные задачи от невыполененных я не смог, поэтому создал алгоритм получения отфильтрованного кверисета."""
        # return Employee.objects.filter(owner=self.request.user).\
        #     annotate(num_tasks=Count('task')).order_by('num_tasks')

        query = Employee.objects.filter(owner=self.request.user)  # Получаем кверисет всех сотрудников пользователя
        emp_dict = {}  # Создаем словарь, который заполним парой (сотрудник: количество невыполненных задач)
        for emp in query:  # Для каждого сотрудника в кверисете найдем количество невыполненных задач
            emp_tasks = Task.objects.filter(employee=emp)  # Среди задач находим задачи сотрудника
            emp_pending = 0
            for task in emp_tasks:
                if task.is_completed is False:
                    emp_pending += 1  # Добавляем 1 к числу невыполненных задач
            emp_dict[emp] = emp_pending  # Добавляем пару: ключ = сотрудник, значение = кол-во невыполненных задач

        sorted_dict = {k: v for k, v in sorted(emp_dict.items(), key=lambda item: item[1])}  # Сортируем по кол-ву задач
        output = list(sorted_dict.keys())  # Оставляем от словаря только отсортированный список ключей (сотрудников)
        return output


class ImportantTasksListAPView(generics.ListAPIView):
    pass

