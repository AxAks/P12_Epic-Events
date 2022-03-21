from rest_framework.permissions import IsAuthenticated

from custom_permissions.lib_permissions import is_manager, is_sales, is_support


class EmployeePermissions(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST']:
            return is_manager(request, view)
        elif request.method in ['GET']:
            return IsAuthenticated


"""
class ClientPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_sales(request, view)


class ContractPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_support(request, view)


class EventPermissions(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return is_support(request, view)


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
