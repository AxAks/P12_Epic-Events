from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, DjangoModelPermissions
from custom_permissions.lib_permissions import is_manager, is_sales, is_support


class EmployeePermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.retrieve_%(model_name)s', '%(app_label)s.list_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


"""
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