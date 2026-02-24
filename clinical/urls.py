from .views import (
    BookAppointmentView,
    UpdateAppointmentStatusView,
    LabReportListView,
    LabReportCreateView,
    AddDepartmentView
    )
from django.urls import path

urlpatterns = [
    path('book/', BookAppointmentView.as_view(), name='book_appointment'),
    path('appointment/<int:pk>/status/<str:status>/', UpdateAppointmentStatusView.as_view(), name='update_appointment_status'),
    path('lab-reports/', LabReportListView.as_view(), name='lab_report_list'),
    path('lab-reports/create/', LabReportCreateView.as_view(), name='lab_report_create'),
    path('dept/add/',AddDepartmentView.as_view(),name='add_dept')
]
