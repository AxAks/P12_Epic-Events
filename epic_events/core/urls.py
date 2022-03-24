from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import EmployeeModelViewSet

app_name = "core"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('employee/', EmployeeModelViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
]
