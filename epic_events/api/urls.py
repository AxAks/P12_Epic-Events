from django.urls import path, include
from rest_framework_nested import routers

from api.views import ClientModelViewSet, ContractModelViewSet, EventModelViewSet, ClientAssignmentModelViewSet, \
    ContractNegotiationAssignmentModelViewSet, EventAssignmentModelViewSet, ContractSignatureAssignmentModelViewSet, \
    ContractPaymentAssignmentModelViewSet

app_name = "api"


router = routers.SimpleRouter()
router.register(r'clients', ClientModelViewSet, basename='clients')

router.register(r'contracts', ContractModelViewSet, basename='contracts')
router.register(r'events', EventModelViewSet, basename='events')
router.register(r'assign_client', ClientAssignmentModelViewSet, basename='client_assignments')
router.register(r'assign_contract_negotiation',
                ContractNegotiationAssignmentModelViewSet,
                basename='contract_negotiation_assignments')
router.register(r'signature_contract', ContractSignatureAssignmentModelViewSet, basename='contract_signatures')
router.register(r'payment_contract', ContractPaymentAssignmentModelViewSet, basename='contract_payments')
router.register(r'assign_event', EventAssignmentModelViewSet, basename='events_assignments')


urlpatterns = [
    path(r'', include(router.urls)),
]
