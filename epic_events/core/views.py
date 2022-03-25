import logging

from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Department, Employee
from core.serializers import EmployeeSerializer, DepartmentSerializer


logger = logging.getLogger('core_app')


class EmployeeModelViewSet(ModelViewSet):
    """
    Endpoint for Employees (users)
    """
    permission_classes = (DjangoModelPermissions, DjangoObjectPermissions)
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create a user along with the department (groups) they belong
        The user gets the permissions of their department
        """
        user = request.user

        self.check_object_permissions(request, self.queryset)

        request_data_copy = request.data.dict()
        department_data = {'department': request_data_copy['department']}
        request_data_copy.pop('department')
        employee_data = request_data_copy

        employee_serializer = self.get_serializer(data=employee_data)
        employee_serializer.is_valid(raise_exception=True)

        department_serializer = DepartmentSerializer(data=department_data)
        department_serializer.is_valid(raise_exception=True)

        department_id = int(department_serializer.initial_data['department'])
        try:
            department_obj = Department.objects.get(pk=department_id)
            serialized_department = DepartmentSerializer(department_obj)
            employee_obj = employee_serializer.save()
            employee_obj.groups.add(department_obj.id)
            headers = self.get_success_headers(employee_serializer.data)
            return Response({'employee': employee_serializer.data, 'department': serialized_department.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        except Department.DoesNotExist:
            return Response({'not_found_error': 'The chosen department does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        user = request.user
        self.check_object_permissions(request, Employee)

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)
