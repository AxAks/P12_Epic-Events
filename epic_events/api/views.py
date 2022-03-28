import logging
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from api.serializers import ClientSerializer, ContractSerializer, EventSerializer

logger = logging.getLogger('api_app')


class ClientModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (DjangoModelPermissions,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create a user along with the department (groups) they belong
        The user gets the permissions of their department
        """
        self.check_object_permissions(request, self.queryset)

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
        client_id = kwargs['client_id']
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


class ContractModelViewSet(ModelViewSet):
    """
    Endpoint for Contracts
    """
    permission_classes = (DjangoModelPermissions,)
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create a contract.
        A contract is linked to a specific client
        """
        self.check_object_permissions(request, self.queryset)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_contract {serializer.data}: by {request.user.first_name} {request.user.last_name}"  # tous les logs à changer (reformater de facon standard)
            f" ({request.user.groups.first().name})")
        return res


class EventModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (DjangoModelPermissions,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create an evant.
        An event is linked to a specific contract
        """
        self.check_object_permissions(request, self.queryset)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        logger.info(
            f"[{datetime.now()}] add_event {serializer.data}: by {request.user.first_name} {request.user.last_name}"  # tous les logs à changer (reformater de facon standard)
            f" ({request.user.groups.first().name})")
        return res
