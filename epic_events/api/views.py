import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event, EventAssignment, ContractAssignment, ClientAssignment
from api.serializers import ClientSerializer, ContractSerializer, EventSerializer, ClientAssignmentSerializer, \
    ContractAssignmentSerializer, EventAssignmentSerializer
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
        logger.info(
            f"[{datetime.now()}] add_client {serializer.data}: User: {request.user.first_name} {request.user.last_name}"  # tous les logs à changer (reformater de facon standard)
            f" ({request.user.groups.first().name})")
        return res

    def retrieve(self, request, **kwargs):
        """
        Returns a specific client by ID
        """
        client_id = kwargs['pk']
        try:
            client = self.queryset.filter(id=client_id).first()
            self.check_object_permissions(request, client)
            serializer = self.serializer_class(client)
            res = Response(serializer.data, status=status.HTTP_200_OK)
            logger.info(f"[{datetime.now()}] retrieve_client {client}"  # tous les logs à changer (reformater de facon standard)
                        f" by {request.user.first_name} {request.user.last_name} ({request.user.groups.first().name})")
            return res
        except Client.DoesNotExist:
            return Response({'not_found_error': 'The requested client does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, **kwargs):
        """
        # Enables the employee to update the information of a specific contract
        """
        client_id = kwargs['pk']
        client = Client.objects.filter(id=client_id).first()
        serializer = self.serializer_class(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        client_obj = serializer.update(client, serializer.validated_data)
        serialized_client = self.serializer_class(client_obj)
        res = Response(serialized_client.data, status=status.HTTP_204_NO_CONTENT)
        logger.info(
            f"[{datetime.now()}] update_client {serialized_client.data}"
            f" by {request.user.first_name} {request.user.last_name} ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_contract {serializer.data}"
            f" by {request.user.first_name} {request.user.last_name} ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
            f"[{datetime.now()}] update_contract {serialized_contract.data}"
            f"by {request.user.first_name} {request.user.last_name} ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_event {serializer.data}:"
            f" by {request.user.first_name} {request.user.last_name}"
            f" ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
            f"[{datetime.now()}] update_event {serialized_event.data}:"
            f" by {request.user.first_name} {request.user.last_name}"
            f" ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] assign_client {serializer.data}:"
            f" by {request.user.first_name} {request.user.last_name}"
            f" ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
        return res


class ContractAssignmentModelViewSet(ModelViewSet):
    """
    Endpoint contract assignments
    """
    permission_classes = (ContractAssignmentPermissions,)
    serializer_class = ContractAssignmentSerializer
    queryset = ContractAssignment.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to assign a Contract to a Sales Employee.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] assign_contract {serializer.data}:"
            f" by {request.user.first_name} {request.user.last_name}"
            f" ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] assign_event {serializer.data}:"
            f" by {request.user.first_name} {request.user.last_name}"
            f" ({request.user.groups.first().name})")
        # tous les logs à changer (reformater de facon standard)
        return res