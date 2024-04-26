from django.urls import path

from tracker.views import EmployeeCreateAPIView, EmployeeRetrieveAPIView, EmployeeUpdateAPIView, EmployeeDestroyAPIView, \
    EmployeeListAPIView, TaskCreateAPIView, TaskRetrieveAPIView, TaskUpdateAPIView, TaskDestroyAPIView, TaskListAPIView, \
    FreeEmployeesListAPIView

app_name = 'api'

urlpatterns = [
    # Сотрудники
    path('employee_create/', EmployeeCreateAPIView.as_view(), name='employee_create'),
    path('employee_retrieve/<int:pk>', EmployeeRetrieveAPIView.as_view(), name='employee_retrieve'),
    path('employee_update/<int:pk>', EmployeeUpdateAPIView.as_view(), name='employee_update'),
    path('employee_destroy/<int:pk>', EmployeeDestroyAPIView.as_view(), name='employee_destroy'),
    path('employee_list/', EmployeeListAPIView.as_view(), name='employee_list'),

    path('free_employees/', FreeEmployeesListAPIView.as_view(), name='free_employee_list'),

    # Задачи
    path('task_create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('task_retrieve/<int:pk>', TaskRetrieveAPIView.as_view(), name='task_retrieve'),
    path('task_update/<int:pk>', TaskUpdateAPIView.as_view(), name='task_update'),
    path('task_destroy/<int:pk>', TaskDestroyAPIView.as_view(), name='task_destroy'),
    path('task_list/', TaskListAPIView.as_view(), name='task_list'),
]
