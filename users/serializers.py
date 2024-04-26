from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = User
        fields = ('email', )


class SignUpSerializer(serializers.ModelSerializer):
    """"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        return super(SignUpSerializer, self).validate(data)
