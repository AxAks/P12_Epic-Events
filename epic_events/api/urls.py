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
router.register(r'client_assignments', ClientAssignmentModelViewSet, basename='client_assignments')
router.register(r'contract_negotiations',
                ContractNegotiationAssignmentModelViewSet,
                basename='contract_negotiation_assignments')
router.register(r'contract_signatures', ContractSignatureAssignmentModelViewSet, basename='contract_signatures')
router.register(r'contract_payments', ContractPaymentAssignmentModelViewSet, basename='contract_payments')
router.register(r'event_assignments', EventAssignmentModelViewSet, basename='event_assignments')


urlpatterns = [
    path(r'', include(router.urls)),
]
