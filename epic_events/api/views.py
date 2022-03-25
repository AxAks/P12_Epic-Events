import logging

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
    permission_classes = (DjangoModelPermissions, DjangoObjectPermissions,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Method to create a user along with the department (groups) they belong
        The user gets the permissions of their department
        """
        user = request.user
        self.check_object_permissions(request, user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, **kwargs):
        """
        Returns a specific client by ID
        """
        user = request.user
        self.check_object_permissions(request, user)

        client_id = kwargs['client_id']
        try:
            client = self.queryset.get(id=client_id)
            serializer = self.serializer_class(client)
            res = Response(serializer.data, status=status.HTTP_200_OK)
            logger.info(f"clients: client infos #{client.id}"  # tous les logs à changer (reformater de facon standard)
                        f" requested by User {request.user.first_name} {request.user.last_name}"
                        f" ({request.user.groups.name})")
            return res
        except Client.DoesNotExist:
            return Response({'not_found_error': 'The requested client does not exist'},
                            status=status.HTTP_404_NOT_FOUND)


class ContractModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (DjangoModelPermissions, DjangoObjectPermissions,)
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class EventModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (DjangoModelPermissions, DjangoObjectPermissions,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
