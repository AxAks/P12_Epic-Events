import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Department
from core.serializers import EmployeeSerializer, DepartmentSerializer
from custom_permissions.permissions import EmployeePermissions

logger = logging.getLogger('core_app')


class EmployeeModelViewSet(ModelViewSet):
    """
    Endpoint to create a user
    """
    permission_classes = (EmployeePermissions,)
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        self.check_object_permissions(request, user)
        request_data_copy = request.data.dict()
        department_data = {'department': request_data_copy['department']}
        request_data_copy.pop('department')
        employee_data = request_data_copy

        employee_serializer = self.get_serializer(data=employee_data)
        employee_serializer.is_valid(raise_exception=True)
        employee_obj = employee_serializer.save()
        department_serializer = DepartmentSerializer(data=department_data)
        department_serializer.is_valid(raise_exception=True)
        department_id = int(department_serializer.initial_data['department'])
        department_obj = Department.objects.get(pk=department_id) # try/except àttre la si pas trouvé, ou trouver un truc propre
        employee_obj.groups.add(department_obj.id)

        headers = self.get_success_headers(employee_serializer.data)
        return Response(employee_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
