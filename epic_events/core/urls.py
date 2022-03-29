from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import EmployeeModelViewSet, PersonalInfosModelViewSet

app_name = "core"

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('my_infos/', PersonalInfosModelViewSet.as_view({
            'get': 'retrieve',
        }
    )),
    path('employee/', EmployeeModelViewSet.as_view({
        'post': 'create',
        'get': 'list'
        }
    )),
    path('employee/<int:pk>', EmployeeModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update'
        }
    )),
]
