import logging
from datetime import datetime

from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from constants import MANAGER
from core.models import Employee
from core.serializers import EmployeeSerializer, DepartmentSerializer
from custom_permissions.permissions import EmployeePermissions

logger = logging.getLogger('core_app')


class EmployeeModelViewSet(ModelViewSet):
    """
    Endpoint for Employees (users)
    """
    permission_classes = (EmployeePermissions,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    filterset_fields = ['id', 'email', 'last_name']

    def create(self, request, *args, **kwargs):
        """
        Method to create a user along with the department (groups) they belong
        The user gets the permissions of their department
        """
        request_data_copy = request.data.dict()
        department_data = {'department': request_data_copy['department']}
        request_data_copy.pop('department')
        employee_data = request_data_copy

        employee_serializer = self.get_serializer(data=employee_data)
        employee_serializer.is_valid(raise_exception=True)

        department_serializer = DepartmentSerializer(data=department_data)
        department_serializer.is_valid(raise_exception=True)

        department_id = int(department_serializer.initial_data['department'])
        department_obj = Group.objects.filter(pk=department_id).first()
        if department_obj:
            serialized_department = DepartmentSerializer(department_obj)
            employee_obj = employee_serializer.save()
            employee_obj.groups.add(department_obj.id)
            if department_obj.id == MANAGER:
                Employee.set_is_staff(employee_obj)
            serialized_employee = EmployeeSerializer(employee_obj)
            headers = self.get_success_headers(employee_serializer.data)
            res = Response({'employee': serialized_employee.data,
                            'department': serialized_department.data if serialized_department.data
                            else 'Not Affected'},
                           status=status.HTTP_201_CREATED, headers=headers)
            logger.info(
                f"[{datetime.now()}] add_employee {employee_obj}"
                f" by: {request.user}")
            return res
        else:
            return Response({'not_found_error': 'The chosen department does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, **kwargs):
        """
        Enables a manager to update the information of a specific employee.
        employee object ID must be known
        """
        employee_id = kwargs['pk']
        employee = Employee.objects.filter(id=employee_id).first()
        if employee:
            serializer = self.serializer_class(employee, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            employee_obj = serializer.update(employee, serializer.validated_data)
            serialized_employee = self.serializer_class(employee_obj)
            res = Response(serialized_employee.data, status=status.HTTP_204_NO_CONTENT)
            logger.info(
                f"[{datetime.now()}] update_employee {employee_obj}"
                f" by {request.user}")
            return res
        else:
            logger.info(
                f"[{datetime.now()}] update_employee by {request.user}"
                f" not_found_error: Employee with ID {employee_id} does not exist")
            return Response({'not_found_error': f'Client with ID {employee_id} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)


class PersonalInfosModelViewSet(ModelViewSet):
    """
    Endpoint that returns the personal infos of the logged employee
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Returns the personal infos of the logged employee
        """
        user = self.queryset.filter(id=request.user.id).first()
        user_department = user.department
        serializer = self.serializer_class(user)
        serialized_department = DepartmentSerializer(user_department)
        res = Response({'current_employee': serializer.data,
                        'department': serialized_department.data if serialized_department.data else 'Not Affected'},
                       status=status.HTTP_200_OK)
        logger.info(
            f"[{datetime.now()}] retrieve_personal_infos"
            f" by {request.user}")
        return res
