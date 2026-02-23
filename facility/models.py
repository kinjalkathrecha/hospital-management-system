from django.db import models
from django.conf import settings

# Room model
class Room(models.Model):
    dept = models.ForeignKey('clinical.Department', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    type = models.CharField(max_length=20, choices=[('GENERAL', 'General'), ('PRIVATE', 'Private'), ('ICU', 'ICU')])
    room_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_days = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.type})"

# Bed model
class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    status = models.BooleanField(default=True) # True for available

    def __str__(self):
        return f"Bed {self.bed_number} in Room {self.room.room_number}"

# Admission model
class Admission(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='admissions')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True)
    admit_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Admission: {self.patient} (Admitted: {self.admit_date})"

# Bill model
class Bill(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='bills')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey('clinical.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    room_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    staff_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PAID', 'Paid'), ('UNPAID', 'Unpaid')], default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient} - Amount: {self.total_amount}"

# Payment model
class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='SUCCESS')

    def __str__(self):
        return f"Payment for Bill {self.bill.id} - Status: {self.payment_status}"

# Staff model 
class Staff(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# StaffAssignment model
class StaffAssignment(models.Model):
    class ProcedureType(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routine Checkup'
        SURGERY = 'SURGERY', 'Surgical Assistance'
        EMERGENCY = 'EMERGENCY', 'Emergency Care'
        MEDICATION = 'MEDICATION', 'Medication Administration'

    class OutcomeStatus(models.TextChoices):
        STABLE = 'STABLE', 'Patient Stabilized'
        IMPROVED = 'IMPROVED', 'Condition Improved'
        CRITICAL = 'CRITICAL', 'Remains Critical'
        DISCHARGED = 'DISCHARGED', 'Discharged'
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assignments')
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='staff_assignments')
    acuity_level = models.PositiveIntegerField(help_text="Patient severity 1-5")
    procedure_type = models.CharField(
        max_length=20, 
        choices=ProcedureType.choices, 
        default=ProcedureType.ROUTINE
    )
    outcome_status = models.CharField(
        max_length=20, 
        choices=OutcomeStatus.choices, 
        default=OutcomeStatus.STABLE
    )
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Staff {self.staff.name} assigned to Patient {self.patient}"
