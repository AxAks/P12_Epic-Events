"""
Lists all queryset for view.
Filters result contents upon type of user
"""
from api.models import Client, Contract, Event, EventAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, ContractPaymentAssignment, ClientAssignment


def clients_queryset(employee):
    """
    Returns the right queryset for the Client view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return Client.objects.filter(contractor__event_contract__assigned_event__employee=employee).distinct()
    else:
        return Client.objects.all()


def contracts_queryset(employee):
    """
    Returns the right queryset for the Contract view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return Contract.objects.filter(event_contract__assigned_event__employee=employee).distinct()
    else:
        return Contract.objects.all()


def events_queryset(employee):
    """
    Returns the right queryset for the Events view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return Event.objects.filter(assigned_event__employee=employee).distinct()
    else:
        return Event.objects.all()


def clientassignments_queryset(employee):
    """
    Returns the right queryset for the Client Assignment view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return ClientAssignment.objects.filter(client__contractor__event_contract__assigned_event__employee=employee)\
            .distinct()
    else:
        return ClientAssignment.objects.all()


def contractnegotiationassignments_queryset(employee):
    """
    Returns the right queryset for the Contract Negotiation Assignment view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return ContractNegotiationAssignment.objects\
            .filter(contract__event_contract__assigned_event__employee=employee).distinct()
    else:
        return ContractNegotiationAssignment.objects.all()


def contractsignatureassignments_queryset(employee):
    """
    Returns the right queryset for the Contract Signature Assignment view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return ContractSignatureAssignment.objects.filter(contract__event_contract__assigned_event__employee=employee)\
            .distinct()
    else:
        return ContractSignatureAssignment.objects.all()


def contractpaymentassignments_queryset(employee):
    """
    Returns the right queryset for the Contract Payment Assignment view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return ContractPaymentAssignment.objects.filter(contract__event_contract__assigned_event__employee=employee)\
            .distinct()
    else:
        return ContractPaymentAssignment.objects.all()


def eventassignments_queryset(employee):
    """
    Returns the right queryset for the Event Assignment view
    Filters access upon type of employee (Manager/Sales/Support)
    """
    if employee.is_support:
        return EventAssignment.objects.filter(employee=employee).distinct()
    else:
        return EventAssignment.objects.all()
