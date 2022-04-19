import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event, EventAssignment, ContractNegotiationAssignment, \
    ContractSignatureAssignment, ClientAssignment, ContractPaymentAssignment
from api.serializers import ClientSerializer, ContractSerializer, EventSerializer, ClientAssignmentSerializer, \
    ContractNegotiationAssignmentSerializer, ContractSignatureAssignmentSerializer, EventAssignmentSerializer, \
    ContractPaymentAssignmentSerializer
from custom_permissions.permissions import EventPermissions, ContractPermissions, ClientPermissions, \
    ClientAssignmentPermissions, ContractAssignmentPermissions, EventAssignmentPermissions

logger = logging.getLogger('api_app')


class ClientModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (ClientPermissions,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

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
        client_obj = self.queryset.filter(id=serializer.data['id']).first()
        logger.info(
            f"[{datetime.now()}] add_client {client_obj}"
            f" by {request.user}")
        return res

    def retrieve(self, request, **kwargs):
        """
        Returns a specific client by ID
        """
        client_id = kwargs['pk']
        client_obj = self.queryset.filter(id=client_id).first()
        self.check_object_permissions(request, client_obj)
        serializer = self.serializer_class(client_obj)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        logger.info(f"[{datetime.now()}] retrieve_client {client_obj}"
                    f" by {request.user.get_full_name()}"
                    f" {request.user.department}")
        return res

    def update(self, request, **kwargs):
        """
        Enables the employee to update the information of a specific contract
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
    queryset = Contract.objects.all()

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
        contract_obj = self.queryset.filter(id=contract.id).first()
        serialized_contract = self.serializer_class(contract_obj)
        res = Response(serialized_contract.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_contract {contract_obj}"
            f" by {request.user}")
        return res

    def retrieve(self, request, **kwargs):
        """
        Returns a specific contract by ID
        """
        contract_id = kwargs['pk']
        contract_obj = self.queryset.filter(id=contract_id).first()
        self.check_object_permissions(request, contract_obj)
        if not contract_obj:
            res = Response({'not_found': 'the requested contract does not exist'}, status=status.HTTP_404_NOT_FOUND)
            logger.info(
                f"[{datetime.now()}] retrieve_contract id:{contract_id} not_found"
                f" by {request.user.get_full_name()}"
                f" {request.user.department}")
            return res
        serializer = self.serializer_class(contract_obj)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        logger.info(f"[{datetime.now()}] retrieve_contract {contract_obj}"
                    f" by {request.user.get_full_name()}"
                    f" {request.user.department}")
        return res

    def update(self, request, **kwargs):
        """
        # Enables the employee to update the information of a specific contract
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
    Endpoint for Clients
    """
    permission_classes = (EventPermissions,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create an event.
        An event is linked to a specific contract
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        headers = self.get_success_headers(serializer.data)
        event_obj = self.queryset.filter(id=event.id).first()
        serialized_event = self.serializer_class(event_obj)
        res = Response(serialized_event.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_event {event_obj}:"
            f" by {request.user}")
        return res

    def update(self, request, **kwargs):
        """
        # Enables the employee to update the information of a specific event
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
    Endpoint client assignments
    """
    permission_classes = (ClientAssignmentPermissions,)
    serializer_class = ClientAssignmentSerializer
    queryset = ClientAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Client to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        client_assignment_obj = self.queryset.filter(id=client_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_client {client_assignment_obj}:"
            f" by {request.user}")
        return res


class ContractNegotiationAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint contract assignments
    """
    permission_classes = (ContractAssignmentPermissions,)
    serializer_class = ContractNegotiationAssignmentSerializer
    queryset = ContractNegotiationAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Contract to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contract_negotiation_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        contract_negotiation_assignment_obj = self.queryset.filter(id=contract_negotiation_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_contract_negotiation {contract_negotiation_assignment_obj}:"
            f" by {request.user}")
        return res


class ContractSignatureAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint contract assignments
    """
    permission_classes = (ContractAssignmentPermissions,)
    serializer_class = ContractSignatureAssignmentSerializer
    queryset = ContractSignatureAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Contract to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signature = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        signature_obj = self.queryset.filter(id=signature.id).first()
        logger.info(
            f"[{datetime.now()}] signature_contract {signature_obj}:"
            f" by {request.user}")
        return res


class ContractPaymentAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint contract assignments
    """
    permission_classes = (ContractAssignmentPermissions,)
    serializer_class = ContractPaymentAssignmentSerializer
    queryset = ContractPaymentAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Contract to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        payment_obj = self.queryset.filter(id=payment.id).first()
        logger.info(
            f"[{datetime.now()}] payment_contract {payment_obj}:"
            f" by {request.user}")
        return res


class EventAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint event assignments
    """
    permission_classes = (EventAssignmentPermissions,)
    serializer_class = EventAssignmentSerializer
    queryset = EventAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign an Event to a Support Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_assignment = serializer.save()
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        event_assignment_obj = self.queryset.filter(id=event_assignment.id).first()
        logger.info(
            f"[{datetime.now()}] assign_event {event_assignment_obj}:"
            f" by {request.user}")
        return res
