from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
ROLE_CHOICES = (
    ('DOCTOR','doctor'),
    ('PATIENT','patient'),
    ('STAFF','staff'),
    ('ADMIN','admin')
)

class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    phone = models.CharField(max_length=15, blank=True)
    emergency_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True) 
    last_login = models.DateTimeField(null=True, blank=True)    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"



class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='doctor_profile'
    )
    dept = models.ForeignKey('clinical.Department', on_delete=models.SET_NULL, null=True, related_name='doctors')
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    charges = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    qualification = models.CharField(max_length=50)
    joining_date = models.DateField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='patient_profile'
    )
    blood_group = models.CharField(max_length=5)
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.get_full_name()