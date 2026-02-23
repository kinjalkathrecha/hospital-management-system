from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions
from .models import User, Doctor, Patient
from .serializers import UserSerializer
from django.utils import timezone
from clinical.models import Appointment, LabReport
from facility.models import Room, Bed, Bill
from django.db.models import Sum,Count
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

def get_dashboard_url(user):
    if user.is_superuser or user.role == 'ADMIN':
        return '/admin/'
    elif user.role == 'DOCTOR':
        return reverse_lazy('doctor_dashboard')
    elif user.role == 'PATIENT':
        return reverse_lazy('patient_dashboard')
    elif user.role == 'STAFF':
        return reverse_lazy('staff_dashboard')
    return reverse_lazy('home')

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return get_dashboard_url(self.request.user)

#registration
class PatientRegistrationView(View):
    template_name = 'register_patient.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='PATIENT'
        )
        Patient.objects.create(
            user=user, 
            address=request.POST.get('address'), 
            city=request.POST.get('city'),
            blood_group=request.POST.get('blood_group', '')
        )
        login(request, user)
        return redirect('patient_dashboard')

class DoctorRegistrationView(View):
    template_name = 'register_doctor.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='DOCTOR'
        )
        doctor_charges = request.POST.get('charges')
        Doctor.objects.create(
            user=user, 
            specialization=request.POST.get('specialization'),
            experience=request.POST.get('experience'),
            qualification=request.POST.get('qualification'),
            charges=doctor_charges
        )
        login(request, user)
        return redirect('doctor_dashboard')

class StaffRegistrationView(View):
    template_name = 'register_staff.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='STAFF'
        )
        login(request, user)
        return redirect('staff_dashboard')

#dashboards
class PatientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/patient_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.request.user.patient_profile
        context['appointments_count'] = Appointment.objects.filter(patient=patient).count()
        context['lab_reports_count'] = LabReport.objects.filter(patient=patient).count()
        context['upcoming_appointments'] = Appointment.objects.filter(
            patient=patient, 
            appointment_date__gte=timezone.now()
        ).order_by('appointment_date')[:5]
        
        bills = Bill.objects.filter(patient=patient)
        context['total_due'] = sum(bill.total_amount for bill in bills if bill.status == 'UNPAID')
        return context

class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/doctor_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user.doctor_profile
        today = timezone.now().date()
        
        today_appointments = Appointment.objects.filter(
            doctor=doctor, 
            appointment_date__date=today
        )
        context['today_count'] = today_appointments.count()
        context['pending_count'] = Appointment.objects.filter(
            doctor=doctor, 
            status='PENDING'
        ).count()
        context['appointments'] = today_appointments[:10]
        return context

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/staff_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_beds = Bed.objects.count()
        occupied_beds = Bed.objects.filter(status=False).count()
        occupancy_rate = (occupied_beds / total_beds * 100) if total_beds > 0 else 0
        
        context['occupancy_rate'] = round(occupancy_rate, 1)
        context['pending_bills_count'] = Bill.objects.filter(status='UNPAID').count()
        return context

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'dashboards/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'ADMIN'

    def get(self, request):
        total_patients = User.objects.filter(role='PATIENT').count()
        total_doctors = User.objects.filter(role='DOCTOR').count()
        
        pending_appointments = Appointment.objects.filter(status='PENDING').count()
        
        # Monthly Revenue Calculation
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        appointment_revenue = Appointment.objects.filter(
            status='COMPLETED',
            appointment_date__gte=start_of_month
        ).aggregate(total=Sum('doctor__charges'))['total'] or 0
        
        lab_revenue = LabReport.objects.filter(
            report_date__gte=start_of_month
        ).aggregate(total=Sum('lab_charge'))['total'] or 0
        
        total_revenue = appointment_revenue + lab_revenue
        
        total_lab_reports = LabReport.objects.count()
        recent_users = User.objects.all().order_by('-date_joined')[:5]

        context = {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'pending_appointments': pending_appointments,
            'total_revenue': total_revenue,
            'total_lab_reports': total_lab_reports,
            'recent_users': recent_users,
        }
        
        return render(request, self.template_name, context)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
