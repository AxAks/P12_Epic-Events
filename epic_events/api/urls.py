from django.urls import path, include
from rest_framework_nested import routers

from api.views import ClientModelViewSet, ContractModelViewSet, EventModelViewSet


app_name = "api"


router = routers.SimpleRouter()
router.register(r'clients', ClientModelViewSet, basename='clients')

clients_router = routers.NestedSimpleRouter(router, r'clients', lookup='clients')
clients_router.register(r'contracts', ContractModelViewSet, basename='contracts')
clients_router.register(r'events', EventModelViewSet, basename='events')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(clients_router.urls)),
]