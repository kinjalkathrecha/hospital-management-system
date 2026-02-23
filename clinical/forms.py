from django import forms
from .models import Appointment, Department, LabReport
from users.models import Doctor, Patient

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
