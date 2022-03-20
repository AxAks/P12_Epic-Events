from rest_framework.permissions import IsAuthenticated

from constants import MANAGER
from core.models import Employee


class IsManager(IsAuthenticated):
    def has_permission(self, request, view):
        employee = Employee.objects.filter(id=request.user.id)
        return bool(employee.department == MANAGER)

    def has_object_permission(self, request, view, obj):
        pass
        return


class IsSales(IsAuthenticated):
    pass


class IsSupport(IsAuthenticated):
    pass
