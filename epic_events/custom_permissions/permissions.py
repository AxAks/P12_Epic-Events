from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from custom_permissions.lib_permissions import is_manager, is_sales, is_support


class EmployeePermissions(IsAuthenticated):
    def has_permission(self, request, view):  # has permissions : quels groups peuvent acceder à la vue des employees
        return is_manager(request, view)

    def has_object_permission(self, request, view, obj):  # has objects permissions : quels groups peut faire quelle action  sur l'Objet
        if request.method in ['POST']:
            return is_manager(request, view)
        elif request.method in ['GET']:
            return IsAuthenticated


class ClientPermissions(IsAuthenticated):  # test client endpoint, permissions à modifier ensuite
    def has_permission(self, request, view):
        return is_manager(request, view) or is_sales(request, view) or is_support(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_sales(request, view)


class ContractPermissions(IsAuthenticated):   # test contract endpoint, permissions à modifier ensuite
    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_sales(request, view)


class EventPermissions(IsAuthenticated):   # test contract endpoint, permissions à modifier ensuite
    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return is_support(request, view)


"""
class ClientAssignmentPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_support(request, view)


class ContractAssignmentPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_support(request, view)


class EventAssignmentPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_support(request, view)
"""
