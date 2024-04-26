from django.db import models

from users.models import User

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


class Employee(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя сотрудника')
    position = models.CharField(max_length=255, verbose_name='Должность сотрудника')
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, verbose_name='Владелец сотрудника')


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название задачи')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE, verbose_name='Родительская задача')
    due_to = models.DateField(**NULLABLE, verbose_name='Срок выполнения')
    is_completed = models.BooleanField(default=False, verbose_name='Статус выполнения задачи')
    employee = models.ForeignKey(Employee, **NULLABLE, on_delete=models.CASCADE, verbose_name='Выполняющий задачу сотрудник')
    owner = models.ForeignKey(User, default=None, on_delete=models.CASCADE, verbose_name='Владелец задачи')


