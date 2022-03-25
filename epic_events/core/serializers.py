import logging

from rest_framework import serializers
from django.contrib.auth.models import Group
from core.models import Employee

logger = logging.getLogger('core_app')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
        read_only_fields = ('name',)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self) -> Employee:
        employee = Employee(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        employee.set_password(password)
        employee.save()

        logger.info(f'New employee registered : {employee.first_name} {employee.last_name}')
        return employee


class EmployeeLoginSerializer(serializers.ModelSerializer):
    """
    Serializer enabling to log in to the api
    """
    class Meta:
        model = Employee
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
