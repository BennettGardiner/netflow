"""
URL configuration for netflow_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import re_path
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

from netflow_app.views import DemandNodeViewSet, ArcViewSet, SolveView, StorageNodeViewSet, SupplyNodeViewSet

router = DefaultRouter()
router.register("api/supply-nodes", SupplyNodeViewSet)
router.register("api/demand-nodes", DemandNodeViewSet)
router.register("api/storage-nodes", StorageNodeViewSet)
router.register(
    "api/arcs",
    ArcViewSet,
    basename="api/arcs",
)
urlpatterns = [re_path("", include(router.urls))]
urlpatterns += [
    path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/solve/', SolveView.as_view(), name='solve'),
    # Swagger UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
