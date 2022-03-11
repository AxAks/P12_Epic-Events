from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import AddEmployeeModelViewSet, AuthenticationAPIView

app_name = "core"

urlpatterns = [
    path('add_employee/', AddEmployeeModelViewSet.as_view({
        'post': 'create'
    })),
    path('login/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
]
