from django.contrib import admin
from .models import Department, Appointment, MedicalRecord, LabReport

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'hod')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'record_date')

@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'report_type', 'report_date')
