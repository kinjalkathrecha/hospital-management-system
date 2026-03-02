from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/clinical/', include('clinical.urls')),
    path('api/v1/facility/', include('facility.urls')),
    path('api/auth/', include('rest_framework.urls')),
]