from rest_framework.viewsets import ModelViewSet

from api.models import Client
from custom_permissions.permissions import ClientPermissions
from api.serializers import ClientSerializer


class ClientModelViewSet(ModelViewSet):
    """
    Endpoint for Clients
    """
    permission_classes = (ClientPermissions,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

