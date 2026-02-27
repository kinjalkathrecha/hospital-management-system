from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
# Department model
class Department(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    hod = models.ForeignKey('users.Doctor', on_delete=models.SET_NULL, null=True,blank=True, related_name='headed_departments')

    def __str__(self):
        return self.name

# Appointment model
class Appointment(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('users.Doctor', on_delete=models.CASCADE, related_name='appointments',blank=True, null=True)
    appointment_date = models.DateTimeField()
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='PENDING')

    def is_past_due(self):
        return self.appointment_date < timezone.now() and self.status in ['PENDING', 'APPROVED']

    def update_overdue_status(self):
        if self.is_past_due():
            if self.status == 'PENDING':
                self.status = 'EXPIRED'
            elif self.status == 'APPROVED':
                self.status = 'COMPLETED'
            self.save()
            return True
        return False

    def clean(self):
    # Only validate on new appointments 
        if not self.pk and self.appointment_date < timezone.now():
            raise ValidationError({'appointment_date': "You cannot book an appointment in the past!"})

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.appointment_date}"

# MedicalRecord model
class MedicalRecord(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey('users.Doctor', on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    record_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.patient} by {self.doctor}"

# LabReport model
class LabReport(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='lab_reports')
    doctor = models.ForeignKey('users.Doctor', on_delete=models.CASCADE, related_name='lab_reports')
    report_type = models.CharField(max_length=100)
    result = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    lab_charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Lab Report: {self.report_type} for {self.patient}"
