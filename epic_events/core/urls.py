from django.urls import path, re_path
from rest_framework_jwt.views import refresh_jwt_token

from core.views import AddEmployeeModelViewSet, AuthenticationAPIView

app_name = "core"

urlpatterns = [
    path('add_employee/', AddEmployeeModelViewSet.as_view({
        'post': 'create'
    })),
    path('login/', AuthenticationAPIView.as_view()),
    re_path('token_refresh/', refresh_jwt_token),
]
