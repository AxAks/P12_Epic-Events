import logging

from rest_framework import serializers
from core.models import Employee, Department

logger = logging.getLogger('django')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('department',)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    department = DepartmentSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self) -> Employee:
        employee = Employee(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            department=self.validated_data['department']
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
