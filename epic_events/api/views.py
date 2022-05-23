import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event

from custom_permissions.permissions import EventPermissions, ContractPermissions, ClientPermissions, \
    ClientAssignmentPermissions, ContractNegotiationAssignmentPermissions, ContractSignatureAssignmentPermissions, \
    ContractPaymentAssignmentPermissions, EventAssignmentPermissions

from api.serializers import ClientSerializer, ContractSerializer, EventSerializer, ClientAssignmentSerializer, \
    ContractNegotiationAssignmentSerializer, ContractSignatureAssignmentSerializer, EventAssignmentSerializer, \
    ContractPaymentAssignmentSerializer

from api.querysets import clients_queryset, contracts_queryset, events_queryset, eventassignments_queryset, \
    contractpaymentassignments_queryset, contractsignatureassignments_queryset, \
    contractnegotiationassignments_queryset, clientassignments_queryset

from api.filters import ContractFilter, EventDatesFilter, ClientAssignmentFilter, \
    ContractNegotiationAssignmentFilter, ContractSignatureAssignmentFilter, ContractPaymentAssignmentFilter, \
    EventAssignmentFilter


logger = logging.getLogger('api_app')


class ClientModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (ClientPermissions,)
    serializer_class = ClientSerializer
    filterset_fields = ['id', 'last_name', 'email']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return clients_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to create a user along with the department (groups) they belong
        The user gets the permissions of their department
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        client_obj = self.get_queryset().filter(id=serializer.data['id']).first()
        logger.info(
            f"[{datetime.now()}] add_client {client_obj}"
            f" by {request.user}")
        return res

    def update(self, request, **kwargs):
        """
        Enables the employee to update the information of a specific contract
        the client id is needed
        """
        client_id = kwargs['pk']
        client = Client.objects.filter(id=client_id).first()
        serializer = self.serializer_class(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        client_obj = serializer.update(client, serializer.validated_data)
        serialized_client = self.serializer_class(client_obj)
        res = Response(serialized_client.data, status=status.HTTP_204_NO_CONTENT)
        logger.info(
            f"[{datetime.now()}] update_client {client_obj}"
            f" by {request.user}")
        return res


class ContractModelViewSet(ModelViewSet):
    """
    Endpoint for Contracts
    """
    permission_classes = (ContractPermissions,)
    serializer_class = ContractSerializer
    filterset_class = ContractFilter
    # search_fields = ['client__last_name', 'client__email']
    # pb avec le filter : only exxact, voir avec search fields si possible de resoudre
    filterset_fields = ['id', 'client__last_name', 'client__email', 'amount_in_cts',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return contracts_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to create a contract.
        A contract is linked to a specific client
        The client must be assigned before the contract is created
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract = serializer.save()
        headers = self.get_success_headers(serializer.data)
        contract_obj = self.get_queryset().filter(id=contract.id).first()
        serialized_contract = self.serializer_class(contract_obj)
        res = Response(serialized_contract.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_contract {contract_obj}"
            f" by {request.user}")
        return res

    def update(self, request, **kwargs):
        """
        Enables the employee to update the information of a specific contract.
        contract id must be known
        """
        contract_id = kwargs['pk']
        contract = Contract.objects.filter(id=contract_id).first()
        serializer = self.serializer_class(contract, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        contract_obj = serializer.update(contract, serializer.validated_data)
        serialized_contract = self.serializer_class(contract_obj)
        res = Response(serialized_contract.data, status=status.HTTP_204_NO_CONTENT)
        logger.info(
            f"[{datetime.now()}] update_contract {contract_obj}"
            f" by {request.user.get_full_name()} "
            f"{request.user.department}")
        return res


class EventModelViewSet(ModelViewSet):
    """
    Endpoint for Events
    """
    permission_classes = (EventPermissions,)
    serializer_class = EventSerializer
    filterset_class = EventDatesFilter
    filterset_fields = ['id', 'contract__client__last_name', 'contract__client__email',
                        'begin_date', 'end_date']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return events_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to create an event.
        An event is linked to a one and only specific contract
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        headers = self.get_success_headers(serializer.data)
        event_obj = self.get_queryset().filter(id=event.id).first()
        serialized_event = self.serializer_class(event_obj)
        res = Response(serialized_event.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_event {event_obj}:"
            f" by {request.user}")
        return res

    def update(self, request, **kwargs):
        """
        Enables the employee to update the information of a specific event.
        Event ID must be provided
        """
        event_id = kwargs['pk']
        event = Event.objects.filter(id=event_id).first()
        serializer = self.serializer_class(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        event_obj = serializer.update(event, serializer.validated_data)
        serialized_event = self.serializer_class(event_obj)
        res = Response(serialized_event.data, status=status.HTTP_204_NO_CONTENT)
        logger.info(
            f"[{datetime.now()}] update_event {event_obj}:"
            f" by {request.user}")
        return res


class ClientAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint for client assignments
    """
    permission_classes = (ClientAssignmentPermissions,)
    serializer_class = ClientAssignmentSerializer
    filterset_class = ClientAssignmentFilter
    filterset_fields = ['id', 'client__last_name', 'client__email',
                        'employee__last_name', 'employee__email',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return clientassignments_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Client to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        client_assignment_obj = self.get_queryset().filter(id=client_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_client {client_assignment_obj}:"
            f" by {request.user}")
        return res


class ContractNegotiationAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint for contract negotation assignments
    """
    permission_classes = (ContractNegotiationAssignmentPermissions,)
    serializer_class = ContractNegotiationAssignmentSerializer
    filterset_class = ContractNegotiationAssignmentFilter
    filterset_fields = ['id', 'contract__client__last_name', 'contract__client__email',
                        'employee__last_name', 'employee__email',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return contractnegotiationassignments_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Contract to a Sales Employee for negotiation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract_negotiation_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        contract_negotiation_assignment_obj = self.get_queryset().filter(id=contract_negotiation_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_contract_negotiation {contract_negotiation_assignment_obj}:"
            f" by {request.user}")
        return res


class ContractSignatureAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint for contract signature assignment/details registration
    """
    permission_classes = (ContractSignatureAssignmentPermissions,)
    serializer_class = ContractSignatureAssignmentSerializer
    filterset_class = ContractSignatureAssignmentFilter
    filterset_fields = ['id', 'contract__client__last_name', 'contract__client__email',
                        'employee__last_name', 'employee__email',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return contractsignatureassignments_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to assign/register a Contract signature details to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signature = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        signature_obj = self.get_queryset().filter(id=signature.id).first()
        logger.info(
            f"[{datetime.now()}] signature_contract {signature_obj}:"
            f" by {request.user}")
        return res


class ContractPaymentAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint for contract payment details/assignments registration
    """
    permission_classes = (ContractPaymentAssignmentPermissions,)
    serializer_class = ContractPaymentAssignmentSerializer
    filterset_class = ContractPaymentAssignmentFilter
    filterset_fields = ['id', 'contract__client__last_name', 'contract__client__email',
                        'employee__last_name', 'employee__email',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return contractpaymentassignments_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to register a payment details for given contract and link the infos to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        payment_obj = self.get_queryset().filter(id=payment.id).first()
        logger.info(
            f"[{datetime.now()}] payment_contract {payment_obj}:"
            f" by {request.user}")
        return res


class EventAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint for event assignments
    """
    permission_classes = (EventAssignmentPermissions,)
    serializer_class = EventAssignmentSerializer
    filterset_class = EventAssignmentFilter
    filterset_fields = ['id', 'event__contract__client__last_name', 'event__contract__client__email',
                        'employee__last_name', 'employee__email',
                        'date_created', 'date_updated']

    def get_queryset(self):
        """
        Queryset related to the view
        takes into account the type of employee and rights given by their department
        """
        return eventassignments_queryset(self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Method to assign an Event to a Support Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        event_assignment_obj = self.get_queryset().filter(id=event_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_event {event_assignment_obj}:"
            f" by {request.user}")
        return res
