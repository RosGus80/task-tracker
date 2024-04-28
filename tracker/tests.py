from django.test import TestCase

from users.models import User
from tracker.models import Employee, Task

from rest_framework.test import APIClient


# Create your tests here.


class ImportantTaskBasicTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create(pk=1, email='test@gmail.com')

        self.employee1 = Employee.objects.create(pk=1, name='employee1', position='position1', owner=self.user)
        self.employee2 = Employee.objects.create(pk=2, name='employee2', position='position2', owner=self.user)

        self.important_task = Task.objects.create(pk=1, name='important_task', employee=None, owner=self.user)
        self.task1 = Task.objects.create(pk=2, name='task1', parent_task=self.important_task, employee=self.employee1,
                                         owner=self.user)

    def test_algorithm(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/important_tasks/')

        self.assertEqual(response.json(), [{'pair_num': 1, 'task': {'pk': 1, 'name': 'important_task'}, 'employee':
                                            {'pk': 2, 'name': 'employee2', 'position': 'position2'}, 'due_to': None}])
        # Тест может порушиться при изменении формата вывода данных. При изменении формата, поменяйте формат нужных
        # данных для теста. Алгоритм должен подобрать свободного сотрудника номер 2 к важной задаче номер 1


class ImportantTaskRelatedEmployeeTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create(pk=1, email='test@gmail.com')

        self.free_employee = Employee.objects.create(pk=1, name='free_employee', position='position', owner=self.user)
        self.related_employee = Employee.objects.create(pk=2, name='related_employee', position='CEO', owner=self.user)

        self.parent_task = Task.objects.create(pk=1, name='parent_task',
                                               employee=self.related_employee, owner=self.user)
        self.important_task = Task.objects.create(pk=2, name='important_task', parent_task=self.parent_task,
                                                  employee=None, owner=self.user)
        self.sub_task = Task.objects.create(pk=3, name='sub_task', parent_task=self.important_task,
                                            employee=self.related_employee, owner=self.user)

    def test_algorithm(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/important_tasks/')

        self.assertEqual(response.json(), [{'pair_num': 1, 'task': {'pk': 2, 'name': 'important_task'}, 'employee':
                                            {'pk': 2, 'name': 'related_employee', 'position': 'CEO'}, 'due_to': None}])

        # Этот тест тоже может порушиться при изменении формата вывода данных. При изменении формата, поменяйте формат
        # нужных данных для теста. Алгоритм должен выбрать важную задачу номер 2 и относящегося к ней сотрудника
        # номер 2, так как он выполняет родительскую задачу, и его нагруженность не больше двух задач, чем у другого
        # сотрудника

