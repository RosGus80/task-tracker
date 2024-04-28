from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
        return Task.objects.filter(owner=self.request.user).order_by('pk')


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
            emp_pending = Task.objects.filter(employee=emp, is_completed=False).count()
            # Среди задач находим невыполненные задачи сотрудника
            emp_dict[emp] = emp_pending  # Добавляем пару: ключ = сотрудник, значение = кол-во невыполненных задач

        sorted_dict = {k: v for k, v in sorted(emp_dict.items(), key=lambda item: item[1])}  # Сортируем по кол-ву задач
        output = list(sorted_dict.keys())  # Оставляем от словаря только отсортированный список ключей (сотрудников)
        return output


class ImportantTasksListAPIView(APIView):
    """Эндпойнт для анализа важных задач. Важными считаются задачи, которые обладают дочерними (зависимыми) задачами,
    но не принятые в работу (не обладают приписанным сотрудником). Анализирует свободных сотрудников и возвращает
    выбранного для каждой задачи оптимального сотрудника и даты выполнения. Требует аутентификации."""

    def get(self, request):
        tasks_queryset = Task.objects.filter(owner=self.request.user, employee=None, is_completed=False)
        # Задачи, не принятые в работу
        important_tasks_queryset = []
        for task in tasks_queryset:
            sub_tasks = Task.objects.filter(parent_task=task).exclude(employee=None, is_completed=True)
            # Дочерние задачи в работе
            if len(sub_tasks) > 0:
                important_tasks_queryset.append(task)

        if not important_tasks_queryset:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Нет важных задач'})

        # Нашли важные задачи и поместили в important_tasks_queryset
        # Для фильтрации списка сотрудников по загруженности используем алгоритм из FreeEmployeesListAPIView

        query = Employee.objects.filter(owner=self.request.user)
        emp_dict = {}
        for emp in query:
            emp_pending = Task.objects.filter(employee=emp, is_completed=False).count()
            emp_dict[emp] = emp_pending

        emp_sorted_dict = {k: v for k, v in sorted(emp_dict.items(), key=lambda item: item[1])}
        emp_sorted_list = list(emp_sorted_dict.keys())

        if not emp_sorted_list:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Нет свободных сотрудников'})

        # Находим сотрудников, выполняющих родительские задачи важных задач (если есть)

        new_tasks_emps = {}

        for task in important_tasks_queryset:
            if not emp_sorted_list:
                break
            chosen_employee = None
            related_employee = None
            free_employee = emp_sorted_list[0]
            free_employee_pending = Task.objects.filter(employee=free_employee, is_completed=False).count()

            if task.parent_task is not None and task.parent_task.employee is not None:
                related_employee = task.parent_task.employee
                related_employee_pending = Task.objects.filter(employee=related_employee, is_completed=False).count()
            else:
                related_employee_pending = -1

            if related_employee_pending != -1:
                if related_employee_pending - free_employee_pending <= 2:
                    chosen_employee = related_employee
                elif free_employee_pending > emp_sorted_list[1]:
                    chosen_employee = emp_sorted_list.pop(0)
                else:
                    chosen_employee = free_employee
            else:
                chosen_employee = free_employee

            new_tasks_emps[task] = chosen_employee

        output = []
        pair_num = 0
        # Вручную генерируем вывод
        for k, v in new_tasks_emps.items():
            pair_num += 1
            task_output = {'pk': k.pk, 'name': k.name}
            employee_output = {'pk': v.pk, 'name': v.name, 'position': v.position}
            output.append({'pair_num': pair_num, 'task': task_output, 'employee': employee_output, 'due_to': k.due_to})

        return Response(output)






