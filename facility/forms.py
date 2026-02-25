from django import  forms
from .models import Admission, Bed, Room

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'doctor', 'room', 'bed']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select'}),
            'bed': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'room': 'Room (Optional)',
            'bed': 'Bed (Optional)',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to only show available beds
        self.fields['bed'].queryset = Bed.objects.filter(status=True)
        # Optional: You could also add some Javascript to filter beds by room in the template
