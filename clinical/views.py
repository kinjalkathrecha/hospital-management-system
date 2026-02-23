from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, View, ListView
from .forms import AppointmentForm, LabReportCreateForm
from .models import Appointment, LabReport

class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'PATIENT'

class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'DOCTOR'

class StaffOrDoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['STAFF', 'DOCTOR', 'ADMIN']

class BookAppointmentView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'book_appointment.html'
    success_url = reverse_lazy('patient_dashboard')

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.patient = self.request.user.patient_profile
        appointment.save()
        messages.success(self.request, 'Appointment booked successfully!')
        return super().form_valid(form)

class UpdateAppointmentStatusView(LoginRequiredMixin, DoctorRequiredMixin, View):
    def get(self, request, pk, status):
        appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
        if status in ['APPROVED', 'COMPLETED', 'CANCELLED']:
            appointment.status = status
            appointment.save()
            messages.success(request, f'Appointment status updated to {status}.')
        return redirect('doctor_dashboard')

class LabReportListView(LoginRequiredMixin, PatientRequiredMixin, ListView):
    model = LabReport
    template_name = 'clinical/lab_report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return LabReport.objects.filter(patient=self.request.user.patient_profile).order_by('-report_date')

class LabReportCreateView(LoginRequiredMixin, StaffOrDoctorRequiredMixin, CreateView):
    model = LabReport
    form_class = LabReportCreateForm
    template_name = 'clinical/lab_report_form.html'
    success_url = reverse_lazy('home') # Will redirect to dashboard in get_success_url

    def form_valid(self, form):
        report = form.save(commit=False)
        if self.request.user.role == 'DOCTOR':
            report.doctor = self.request.user.doctor_profile
        # If staff, what doctor? Model requires a doctor.
        # Let's check the model definition again.
        report.save()
        messages.success(self.request, 'Lab Report created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.role == 'DOCTOR':
            return reverse_lazy('doctor_dashboard')
        elif self.request.user.role == 'STAFF':
            return reverse_lazy('staff_dashboard')
        return reverse_lazy('home')
