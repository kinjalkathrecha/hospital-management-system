from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('clinical/', include('clinical.urls')),
    path('facility/', include('facility.urls')),
]
