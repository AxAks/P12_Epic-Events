from rest_framework.permissions import IsAuthenticated

from constants import MANAGER, SALES, SUPPORT
from core.models import Employee


class IsManager(IsAuthenticated): # mais en fait il faut faire des permissions par Objet plutot ...
    def has_permission(self, request, view):
        employee = Employee.objects.get(id=request.user.id)
        return employee.groups.filter(id=MANAGER).exists()

    def has_object_permission(self, request, view, obj):
        pass
        return


class IsSales(IsAuthenticated):
    pass


class IsSupport(IsAuthenticated):
    pass
