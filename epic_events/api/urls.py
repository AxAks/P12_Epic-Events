from django.urls import path

from api.views import ClientModelViewSet

app_name = "api"

urlpatterns = [
    path('clients/', ClientModelViewSet.as_view({'get': 'list'})),
    path('clients/<int:client_id>', ClientModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),  # 'delete': 'destroy'
]
