from django.urls import path

from api.views import ClientModelViewSet, ContractModelViewSet, EventModelViewSet

app_name = "api"

urlpatterns = [
    path('clients/', ClientModelViewSet.as_view({'get': 'list'})),
    path('clients/<int:client_id>', ClientModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),  # 'delete': 'destroy'
    path('contracts/', ContractModelViewSet.as_view({'get': 'list'})),
    path('contracts/<int:contract_id>', ContractModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),  # 'delete': 'destroy'
    path('events/', EventModelViewSet.as_view({'get': 'list'})),
    path('events/<int:event_id>', ContractModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),  # 'delete': 'destroy'
]
