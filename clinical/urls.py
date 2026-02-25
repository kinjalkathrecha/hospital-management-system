from .views import (
    BookAppointmentView,
    UpdateAppointmentStatusView,
    LabReportListView,
    LabReportCreateView,
    AddDepartmentView,
    MedicalRecordCreateView,
    MedicalRecordListView,
    MedicalRecordDetailView,
    MedicalRecordUpdateView,
    MedicalRecordDeleteView
    )
from django.urls import path

urlpatterns = [
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('appointment/<int:pk>/status/<str:status>/', UpdateAppointmentStatusView.as_view(), name='update_appointment_status'),
    path('lab-reports/', LabReportListView.as_view(), name='lab_report_list'),
    path('lab-reports/create/', LabReportCreateView.as_view(), name='lab_report_create'),
    path('dept/add/',AddDepartmentView.as_view(),name='add_dept'),
    path('medical-records/', MedicalRecordListView.as_view(), name='medical_record_list'),
    path('medical-record/create/', MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('medical-record/create/<int:patient_id>/', MedicalRecordCreateView.as_view(), name='medical_record_create_with_patient'),
    path('medical-record/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medical-record/<int:pk>/edit/', MedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('medical-record/<int:pk>/delete/', MedicalRecordDeleteView.as_view(), name='medical_record_delete'),
]
