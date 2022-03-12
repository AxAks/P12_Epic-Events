import logging

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.serializers import EmployeeSerializer


logger = logging.getLogger('core_app')


class AddEmployeeModelViewSet(ModelViewSet):
    """
    Endpoint to create a user
    """
    permission_classes = (AllowAny,) # Only ADmin Group !! à changer
    serializer_class = EmployeeSerializer
