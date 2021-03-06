"""epic_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-auth/', RedirectView.as_view(pattern_name='rest_framework:login')),

    path('', include('core.urls', namespace='core')),
    path('', RedirectView.as_view(pattern_name='admin:index')),
    path('core/', RedirectView.as_view(pattern_name='admin:index')),

    path('api/', include('api.urls', namespace='api')),
    path('api/', RedirectView.as_view(pattern_name='admin:index')),

]
