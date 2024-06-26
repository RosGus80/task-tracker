from rest_framework import serializers

from tracker.models import Employee, Task
from users.serializers import UserSerializer


class EmployeeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        exclude = ('owner',)


class EmployeeRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tasks = serializers.SerializerMethodField()
    pending_tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        queryset = Task.objects.filter(employee=obj)
        task_list = []
        for task in queryset:
            task_list.append({'pk': task.pk, 'name': task.name, 'is_completed': task.is_completed})
        return task_list

    def get_pending_tasks(self, obj):
        return Task.objects.filter(employee=obj, is_completed=False).count()

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения сотрудников при сериализации их задач.
    Создан, чтобы избежать обращения сериализатора задач к самому себе,
    как при использовании EmployeeRetrieveSerializer"""

    class Meta:
        model = Employee
        fields = ('id', 'name', 'position')


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ('owner', )


    def validate(self, attrs):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        parent_task = attrs.get('parent_task')
        employee = attrs.get('employee')

        if parent_task is not None:
            if parent_task.owner != user:
                raise serializers.ValidationError('Указанная родительская задача не принадлежит вам')
        if employee is not None:
            if employee.owner != user:
                raise serializers.ValidationError('Указанный сотрудник не принадлежит вам')
        return super(TaskCreateSerializer, self).validate(attrs)


class TaskRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    employee = EmployeeForTaskSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
