from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.views import UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token),
    path('api/users/', include('users.urls')),
    path('api/clinical/', include('clinical.urls')),
    path('api/facility/', include('facility.urls')),
    path('api/auth/', include('rest_framework.urls')),
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]