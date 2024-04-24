from django.urls import path

from tracker.views import EmployeeCreateAPIView, EmployeeRetrieveAPIView, EmployeeUpdateAPIView, EmployeeDestroyAPIView, \
    EmployeeListAPIView, TaskCreateAPIView, TaskRetrieveAPIView, TaskUpdateAPIView, TaskDestroyAPIView, TaskListAPIView

app_name = 'api'

urlpatterns = [
    # Сотрудники
    path('employee_create/', EmployeeCreateAPIView.as_view(), name='employee_create'),
    path('employee_retrieve/<int:pk>', EmployeeRetrieveAPIView.as_view(), name='employee_retrieve'),
    path('employee_update/', EmployeeUpdateAPIView.as_view(), name='employee_update'),
    path('employee_destroy/', EmployeeDestroyAPIView.as_view(), name='employee_destroy'),
    path('employee_list/', EmployeeListAPIView.as_view(), name='employee_list'),

    # Задачи
    path('task_create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('task_retrieve/<int:pk>', TaskRetrieveAPIView.as_view(), name='task_retrieve'),
    path('task_update/', TaskUpdateAPIView.as_view(), name='task_update'),
    path('task_destroy/', TaskDestroyAPIView.as_view(), name='task_destroy'),
    path('task_list/', TaskListAPIView.as_view(), name='task_list'),
]
