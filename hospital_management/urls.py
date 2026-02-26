from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView,LoginView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, DashboardRedirectView , HomeView
router = DefaultRouter()
router.register(r'users', UserViewSet)
handler403 = 'users.views.error_403'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('accounts/profile/', DashboardRedirectView.as_view(), name='profile_redirect'),

    path('', include('users.urls')), 
    path('',include('clinical.urls')),
    path('',include('facility.urls')),

    path('api/', include(router.urls)),
]