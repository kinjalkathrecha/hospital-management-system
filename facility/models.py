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
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE') 

    class Meta:
        unique_together = ('room', 'bed_number')

    def __str__(self):
        return f"Bed {self.bed_number} in Room {self.room.room_number}"
    
# Admission model
class Admission(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='admissions')
    doctor = models.ForeignKey('users.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='admissions')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)

    admit_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
    ('ADMITTED', 'Admitted'),
    ('DISCHARGED', 'Discharged'),
    ('TRANSFERRED', 'Transferred'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ADMITTED')
    def __str__(self):
        return f"Admission: {self.patient} (Admitted: {self.admit_date})"

    @property
    def length_of_stay(self):
        from django.utils import timezone
        
        # Convert everything to a date object (strips time)
        admit_date = self.admit_date.date()
        end_date = self.discharge_date.date() if self.discharge_date else timezone.now().date()
        
        delta = end_date - admit_date
        # Adding 1 ensures that admitting and discharging on the same day counts as 1 day
        return delta.days + 1

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pk and self.bed and not self.bed.status:
             raise ValidationError(f"Bed {self.bed.bed_number} is already occupied.")
        
        if self.discharge_date and self.discharge_date < self.admit_date:
            raise ValidationError("Discharge date cannot be earlier than admit date.")

        if self.status == 'DISCHARGED' or self.discharge_date:
            # Check for unpaid bills linked to THIS admission
            unpaid_bills = self.admission_bills.filter(status='UNPAID').exists()
            if unpaid_bills:
                raise ValidationError("Cannot discharge patient until all bills for this admission are PAID.")


    def save(self, *args, **kwargs):
        self.full_clean()
        
        is_new = self.pk is None
        
        if is_new and self.bed:
            self.bed.status = False 
            self.bed.save()
            
        if self.status == 'DISCHARGED':
            if self.bed:
                self.bed.status = True  
                self.bed.save()
                
                
        super().save(*args, **kwargs)

    

# Bill model
class Bill(models.Model):
    patient = models.ForeignKey('users.Patient', on_delete=models.CASCADE, related_name='bills')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='admission_bills')
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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='staff_profile',
        null=True, blank=True
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    dept = models.ForeignKey('clinical.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Staff)"

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
        return f"Staff {self.staff.user.get_full_name()} assigned to Patient {self.patient}"


