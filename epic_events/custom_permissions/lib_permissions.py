"""
Functions lib for the custom_permissions for the app
"""
from constants import MANAGER, SALES, SUPPORT
from core.models import Employee


def get_employee(request):
    return Employee.objects.get(id=request.user.id)


def is_manager(request, view) -> bool:
    employee = get_employee(request)
    return employee.groups.filter(id=MANAGER).exists()


def is_sales(request, view) -> bool:
    employee = get_employee(request)
    return employee.groups.filter(id=SALES).exists()


def is_support(request, view) -> bool:
    employee = get_employee(request)
    return employee.groups.filter(id=SUPPORT).exists()
