from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView
from .views import (
    HomeView, UserLoginView,  
    PatientRegistrationView, DoctorRegistrationView, StaffRegistrationView, AdminAddDoctorView,
    PatientDashboardView, DoctorDashboardView, StaffDashboardView,AdminDashboardView,
    UserViewSet
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/patient/', PatientRegistrationView.as_view(), name='register_patient'),
    path('register/doctor/', DoctorRegistrationView.as_view(), name='register_doctor'),
    path('dashboard/admin/add-doctor/', AdminAddDoctorView.as_view(), name='admin_add_doctor'),
    path('register/staff/', StaffRegistrationView.as_view(), name='register_staff'),
 
    path('dashboard/admin/',AdminDashboardView.as_view(),name='admin_dashboard'),
    path('dashboard/patient/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),

]