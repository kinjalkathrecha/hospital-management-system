from django.urls import path
from .views import (
    HomeView,  
    PatientRegistrationView, DoctorRegistrationView, StaffRegistrationView, AdminAddDoctorView,
    PatientDashboardView, DoctorDashboardView, StaffDashboardView,AdminDashboardView,
    UserViewSet,
    DashboardRedirectView,AdminAddStaffView
)

urlpatterns = [
   
    path('accounts/profile/', DashboardRedirectView.as_view(), name='profile_redirect'),
    path('register/patient/', PatientRegistrationView.as_view(), name='register_patient'),
    path('register/doctor/', DoctorRegistrationView.as_view(), name='register_doctor'),
    path('register/staff/', StaffRegistrationView.as_view(), name='register_staff'),
    path('dashboard/admin/add-doctor/', AdminAddDoctorView.as_view(), name='add_doctor'),
    path('dashboard/admin/add-staff/', AdminAddStaffView.as_view(), name='add_staff'),

    path('dashboard/admin/',AdminDashboardView.as_view(),name='admin_dashboard'),
    path('dashboard/patient/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('dashboard/doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('dashboard/staff/', StaffDashboardView.as_view(), name='staff_dashboard'),

]