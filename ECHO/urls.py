"""
URL configuration for ECHO project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from news_api.views import MyTokenObtainPairView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Echo API",
        default_version='v1',
        description="An API that serves the latest news from all over the world",
        contact=openapi.Contact(email="ibeabuchibenson@gmial.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa

    path('account/', include('account.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa
    path('api/', include("news_api.urls")),
    path('', include('news.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # noqa
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # noqa
