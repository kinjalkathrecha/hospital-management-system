from django.urls import path
from .views import (
    RoomListView, ToggleBedStatusView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    ActiveAdmissionListView, AdmissionDetailView, DischargePatientView, AdmissionCreateView
)

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    path('bed/<int:pk>/toggle/', ToggleBedStatusView.as_view(), name='toggle_bed_status'),
    
    # New Admission URLs
    path('admissions/active/', ActiveAdmissionListView.as_view(), name='active_admission_list'),
    path('admissions/add/', AdmissionCreateView.as_view(), name='admission_create'),
    path('admissions/<int:pk>/', AdmissionDetailView.as_view(), name='admission_detail'),
    path('admissions/<int:pk>/discharge/', DischargePatientView.as_view(), name='discharge_patient'),
]


