from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor

class PatientRegistrationForm(UserCreationForm):
    GENDER_CHOICES= [
        ('','Select gender'),
        ('MALE','male'),
        ('FEMALE','female'),
        ('OTHER','other')
    ]

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,required=True,label="gender")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    city = forms.CharField(max_length=100)
    BLOOD_GROUP_CHOICES = [
            ('', 'Select Blood Group'), # Optional empty label
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
        ]
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES, 
        required=False,
        label="Blood Group"
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PATIENT'
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                blood_group=self.cleaned_data['blood_group']
            )
        return user

class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    specialization = forms.CharField(max_length=100)
    experience = forms.IntegerField()
    qualification = forms.CharField(max_length=50)
    charges = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'DOCTOR'
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                specialization=self.cleaned_data['specialization'],
                experience=self.cleaned_data['experience'],
                qualification=self.cleaned_data['qualification'],
                charges=self.cleaned_data['charges']
            )
        return user

class StaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'STAFF'
        if commit:
            user.save()
        return user
