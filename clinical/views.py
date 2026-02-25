from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, View, ListView, DetailView, UpdateView, DeleteView
from .forms import AppointmentForm, LabReportCreateForm, AddDepartmentForm, MedicalRecordForm
from .models import Appointment, LabReport, Department, MedicalRecord

class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'PATIENT'

class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'DOCTOR'

class StaffOrDoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['STAFF', 'DOCTOR', 'ADMIN']

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

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
        report.save()
        messages.success(self.request, 'Lab Report created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.role == 'DOCTOR':
            return reverse_lazy('doctor_dashboard')
        elif self.request.user.role == 'STAFF':
            return reverse_lazy('staff_dashboard')
        return reverse_lazy('home')

class AddDepartmentView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Department
    form_class = AddDepartmentForm
    template_name = 'clinical/add_dept.html'
    success_url = reverse_lazy('admin_dashboard')

    def form_valid(self, form):
        dept = form.save()
        messages.success(self.request, 'Department added successfully!')
        return super().form_valid(form)

class MedicalRecordCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'clinical/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.kwargs.get('patient_id')
        if patient_id:
            initial['patient'] = patient_id
        return initial

    def form_valid(self, form):
        record = form.save(commit=False)
        record.doctor = self.request.user.doctor_profile
        record.save()
        messages.success(self.request, 'Medical Record created successfully!')
        return super().form_valid(form)

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'clinical/medical_record_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'DOCTOR':
            return MedicalRecord.objects.all().order_by('-record_date')
        elif user.role == 'PATIENT':
            return MedicalRecord.objects.filter(patient=user.patient_profile).order_by('-record_date')
        return MedicalRecord.objects.none()

class MedicalRecordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MedicalRecord
    template_name = 'clinical/medical_record_detail.html'
    context_object_name = 'record'

    def test_func(self):
        user = self.request.user
        record = self.get_object()
        if user.role == 'DOCTOR':
            return True
        if user.role == 'PATIENT':
            return record.patient == user.patient_profile
        return False

class MedicalRecordUpdateView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'clinical/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def form_valid(self, form):
        messages.success(self.request, 'Medical Record updated successfully!')
        return super().form_valid(form)

class MedicalRecordDeleteView(LoginRequiredMixin, DoctorRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'clinical/medical_record_confirm_delete.html'
    success_url = reverse_lazy('medical_record_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Medical Record deleted successfully!')
        return super().delete(request, *args, **kwargs)