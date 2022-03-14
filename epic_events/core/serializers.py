import logging


from rest_framework import serializers
from core.models import Employee, Profile

logger = logging.getLogger('django')


class EmployeeSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'password', 'password2']
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
        logger.info(f'New user registered : {employee.username}')
        return employee


class EmployeeLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
