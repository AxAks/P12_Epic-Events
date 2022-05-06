"""
Lists all queryset for view.
Filters result contents upon type of user
"""
from api.models import Client, Contract, Event, EventAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, ContractPaymentAssignment, ClientAssignment


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


def clientassignments_queryset(employee):
    if employee.is_support:
        return ClientAssignment.objects.filter(client__contractor__event_contract__assigned_event__employee=employee)
    else:
        return ClientAssignment.objects.all()


def contractnegotiationassignments_queryset(employee):
    if employee.is_support:
        return ContractNegotiationAssignment.objects.filter(contract__event_contract__assigned_event__employee=employee)
    else:
        return ContractNegotiationAssignment.objects.all()


def contractsignatureassignments_queryset(employee):
    if employee.is_support:
        return ContractSignatureAssignment.objects.filter(contract__event_contract__assigned_event__employee=employee)
    else:
        return ContractSignatureAssignment.objects.all()


def contractpaymentassignments_queryset(employee):
    if employee.is_support:
        return ContractPaymentAssignment.objects.filter(contract__event_contract__assigned_event__employee=employee)
    else:
        return ContractPaymentAssignment.objects.all()


def eventassignments_queryset(employee):
    if employee.is_support:
        return EventAssignment.objects.filter(employee=employee)
    else:
        return EventAssignment.objects.all()

