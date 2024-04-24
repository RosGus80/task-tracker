from django.urls import path

from tracker.views import EmployeeCreateAPIView, EmployeeRetrieveAPIView, EmployeeUpdateAPIView, EmployeeDestroyAPIView, \
    EmployeeListAPIView

app_name = 'api'

urlpatterns = [
    path('employee_create/', EmployeeCreateAPIView.as_view(), name='employee_create'),
    path('employee_retrieve/<int:pk>', EmployeeRetrieveAPIView.as_view(), name='employee_retrieve'),
    path('employee_update/', EmployeeUpdateAPIView.as_view(), name='employee_update'),
    path('employee_destroy/', EmployeeDestroyAPIView.as_view(), name='employee_destroy'),
    path('employee_list/', EmployeeListAPIView.as_view(), name='employee_list'),
]
