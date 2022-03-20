import logging

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from core.serializers import EmployeeSerializer, EmployeeLoginSerializer
from custom_permissions import IsManager

logger = logging.getLogger('core_app')


class AddEmployeeModelViewSet(ModelViewSet):
    """
    Endpoint to create a user
    """
    permission_classes = (IsManager,)
    serializer_class = EmployeeSerializer


class AuthenticationTokenView(TokenObtainPairView):
    """
    Endpoint to Signup and get authentication Token
    """
    permission_classes = (AllowAny,)
    serializer_class = EmployeeLoginSerializer
