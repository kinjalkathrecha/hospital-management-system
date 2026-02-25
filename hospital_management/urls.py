from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, DashboardRedirectView 
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    
    path('accounts/profile/', DashboardRedirectView.as_view(), name='profile_redirect'),

    path('', include('users.urls')), 
    path('',include('clinical.urls')),
    path('',include('facility.urls')),

    path('api/', include(router.urls)),
]