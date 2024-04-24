from django.contrib import admin

from tracker.models import Employee, Task


# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'owner')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_task', 'employee', 'owner')