from django.urls import path, include
from rest_framework_nested import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import EmployeeModelViewSet, PersonalInfosModelViewSet

app_name = "core"


router = routers.SimpleRouter()
router.register(r'employees', EmployeeModelViewSet, basename='employees')

employees_router = routers.NestedSimpleRouter(router, r'employees', lookup='employees')
employees_router.register(r'employees', EmployeeModelViewSet, basename='employees')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(employees_router.urls)),
    path('login/', TokenObtainPairView.as_view()),
    path('token_refresh/', TokenRefreshView.as_view()),
    path('my_infos/', PersonalInfosModelViewSet.as_view({
        'get': 'retrieve',
    }
    )),
]