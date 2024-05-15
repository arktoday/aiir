"""
URL configuration for access_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from access.views import AccessViewSet, SourceViewSet, UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    
    path('api/user/', UserViewSet.as_view({'post': 'create_user'}), name='create_user'),
    path('api/user/', UserViewSet.as_view({'get': 'get'}), name='all_users'),
    
    path('api/source/', SourceViewSet.as_view({'post': 'create_source'}), name='create_source'),
    path('api/source/', SourceViewSet.as_view({'get': 'get'}), name='all_sources'),
    
    path('api/access/', AccessViewSet.as_view({'post': 'set_access'}), name='set_access_to_user'),
    path('api/access/', AccessViewSet.as_view({'delete': 'delete'}), name='delete_user_access'),
    path('api/access/', AccessViewSet.as_view({'get': 'get'}), name='check_access'),
]
