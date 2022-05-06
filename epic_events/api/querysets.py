"""
Lists all queryset for view.
Filters result contents upon type of user
"""
from api.models import Client, Contract, Event


def clients_queryset(employee):
    if employee.is_support:
        return Client.objects.filter(contractor__event_contract__assigned_event__employee=employee)
    else:
        return Client.objects.all()


def contracts_queryset(employee):
    if employee.is_support:
        return Contract.objects.filter(event_contract__assigned_event__employee=employee)
    else:
        return Contract.objects.all()


def events_queryset(employee):
    if employee.is_support:
        return Event.objects.filter(assigned_event__employee=employee)
    else:
        return Event.objects.all()
