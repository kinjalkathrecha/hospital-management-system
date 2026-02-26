from django import  forms
from .models import Admission, Bed, Room

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'doctor', 'room', 'bed']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'room': forms.Select(attrs={'class': 'form-select', 'id': 'id_room'}),
            'bed': forms.Select(attrs={'class': 'form-select', 'id': 'id_bed'}),
        }
        labels = {
            'room': 'Assign Room',
            'bed': 'Assign Bed',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['bed'].queryset = Bed.objects.filter(status='AVAILABLE')
        
        
        # 3. Add a placeholder for a better UI
        self.fields['bed'].empty_label = "Select an available bed"
        self.fields['room'].empty_label = "Select a room"
    
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['dept', 'room_number', 'type', 'room_charge']
        
        widgets = {
            'dept': forms.Select(attrs={'class': 'form-select'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 101'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'room_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Charge per day'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dept'].empty_label = "Select Department"

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['room', 'bed_number']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'bed_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. B-101'
            }),
            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Only show rooms that are active/available if you have that logic
        self.fields['room'].empty_label = "--- Select Room ---"