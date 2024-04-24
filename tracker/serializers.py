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

    def get_tasks(self, obj):
        return Task.objects.filter(employee=obj)

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'position')


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ('owner', )


class TaskRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    employee = EmployeeForTaskSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


