from rest_framework.permissions import IsAuthenticated

from constants import MANAGER, SALES, SUPPORT
from core.models import Employee


class IsManager(IsAuthenticated):
    def has_permission(self, request, view):
        employee = Employee.objects.get(id=request.user)  # request.user.id = None !!!
        return bool(MANAGER in employee.groups)

    def has_object_permission(self, request, view, obj):
        pass
        return


class IsSales(IsAuthenticated):
    pass


class IsSupport(IsAuthenticated):
    pass
