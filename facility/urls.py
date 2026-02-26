from django.urls import path
from .views import (
    RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView,
    ActiveAdmissionListView, AdmissionDetailView, DischargePatientView, AdmissionCreateView,
    BedListView,BedCreateView,BedUpdateView,BedDeleteView
)

urlpatterns = [
    # room URLs
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/add/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room_delete'),
    
    # New Admission URLs
    path('admissions/active/', ActiveAdmissionListView.as_view(), name='active_admission_list'),
    path('admissions/add/', AdmissionCreateView.as_view(), name='admission_create'),
    path('admissions/<int:pk>/', AdmissionDetailView.as_view(), name='admission_detail'),
    path('admissions/<int:pk>/discharge/', DischargePatientView.as_view(), name='discharge_patient'),

    # bed URLs
    path('beds/', BedListView.as_view(), name='bed_list'),
    path('beds/add/', BedCreateView.as_view(), name='bed_create'),
    path('beds/<int:pk>/edit/',BedUpdateView.as_view(), name='bed_update'),
    path('beds/<int:pk>/delete/',BedDeleteView.as_view(), name='bed_delete'),
]


