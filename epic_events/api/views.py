from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event
from custom_permissions.permissions import ClientPermissions, ContractPermissions, EventPermissions
from api.serializers import ClientSerializer, ContractSerializer, EventSerializer


class ClientModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (ClientPermissions,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ContractModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (ContractPermissions,)
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class EventModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (EventPermissions,)
    serializer_class = EventSerializer
    queryset = Event.objects.all()
