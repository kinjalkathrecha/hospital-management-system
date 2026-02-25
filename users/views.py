from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import TemplateView, View, CreateView
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions
from .models import User, Doctor, Patient
from .serializers import UserSerializer
from django.utils import timezone
from clinical.models import Appointment, LabReport
from facility.models import Room, Bed, Bill
from django.db.models import Sum
from .forms import PatientRegistrationForm, DoctorRegistrationForm, StaffRegistrationForm

class HomeView(TemplateView):
    template_name = 'home.html'

def get_dashboard_url(user):
    if user.is_superuser or user.role == 'ADMIN':
        return reverse_lazy('admin_dashboard')
    elif user.role == 'DOCTOR':
        return reverse_lazy('doctor_dashboard')
    elif user.role == 'PATIENT':
        return reverse_lazy('patient_dashboard')
    elif user.role == 'STAFF':
        return reverse_lazy('staff_dashboard')
    return reverse_lazy('home')

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return get_dashboard_url(self.request.user)

class PatientRegistrationView(CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'register_patient.html'
    success_url = reverse_lazy('patient_dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class DoctorRegistrationView(CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'register_doctor.html'
    success_url = reverse_lazy('doctor_dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class StaffRegistrationView(CreateView):
    model = User
    form_class = StaffRegistrationForm
    template_name = 'register_staff.html'
    success_url = reverse_lazy('staff_dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class AdminAddDoctorView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'register_doctor.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'ADMIN'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Doctor registered successfully!')
        return redirect(self.success_url)

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
        context['total_due'] = bills.filter(status='UNPAID').aggregate(total=Sum('total_amount'))['total'] or 0
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
        
        # Monthly Revenue Calculation based on Paid Bills
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_revenue = Bill.objects.filter(
            status='PAID',
            created_at__gte=start_of_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
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
