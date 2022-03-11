import jwt
import logging

from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
#from rest_framework_simplejwt.serializers import jwt_payload_handler

from EpicEvents import settings
from core.models import Employee
from core.serializers import EmployeeSerializer, EmployeeLoginSerializer


logger = logging.getLogger('core_app')


class AddEmployeeModelViewSet(ModelViewSet):
    """
    Endpoint to create a user
    """
    permission_classes = (AllowAny,)
    serializer_class = EmployeeSerializer

# Not used with SimpleJWt ... à voir
class AuthenticationAPIView(APIView):
    """
    Endpoint to Signup and get authentication Token
    """
    permission_classes = (AllowAny,)
    serializer_class = EmployeeLoginSerializer

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Enables the user to send their infos to login
        """
        try:
            username = request.data['username']
            password = request.data['password']

            user = get_object_or_404(Employee.objects.filter(username=username))
            if user and check_password(password, user.password):
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {'name': f"{user.first_name} {user.last_name}", 'token': token}
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    logger.info(f'User connection for {user.username} : successful')
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                logger.warning({'users': 'Unsuccessful connection attempt'})
                return Response({'error': 'can not authenticate with the given credentials'
                                          ' or the account has been deactivated'},
                                status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            logger.warning({'users': 'Unsuccessful connection attempt'})
            return Response({'error': 'please provide valid username and password'})