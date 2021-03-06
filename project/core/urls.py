"""activity_schedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from apps.activities.views import ActivityViewSet, RetrieveSurvey


router = routers.DefaultRouter()
router.register(r'activities', viewset=ActivityViewSet)
router.register(r'surveys', viewset=RetrieveSurvey)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('openapi', get_schema_view(  # OpenAPI Schema generator
        title="TrueHome Backend Test",
        version="1.0"
    ), name='openapi-schema')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
