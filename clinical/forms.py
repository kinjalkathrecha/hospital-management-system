from django import forms
from .models import Appointment, Department, LabReport,Department

class AppointmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'status']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'PENDING'

class LabReportCreateForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['patient', 'doctor', 'report_type', 'result', 'lab_charge']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'report_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Blood Test, X-Ray'}),
            'result': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lab_charge': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        FLOOR_CHOICES = [
        ('1', '1st Floor'),
        ('2', '2nd Floor'),
        ('3', '3rd Floor'),
        ('4', '4th Floor'),
        ('5', '5th Floor'),
        ('6', '6th Floor'),
    ]

        model = Department
        fields = ['name', 'floor', 'hod']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Anesthesiology'}),
            'floor': forms.Select(attrs={'class': 'form-control'}, choices=FLOOR_CHOICES),
            'hod': forms.Select(attrs={'class': 'form-control'})
        }
