from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Room, Bed

from django.utils import timezone
from .models import Room, Bed, Admission
from .forms import AdmissionForm
from clinical.models import MedicalRecord, LabReport

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['STAFF', 'ADMIN']

class AdmissionCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Admission
    form_class = AdmissionForm
    template_name = 'hospital_facility/admission_form.html'
    success_url = reverse_lazy('active_admission_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient admitted successfully!')
        return super().form_valid(form)


class ActiveAdmissionListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Admission
    template_name = 'hospital_facility/active_admission_list.html'
    context_object_name = 'admissions'

    def get_queryset(self):
        return Admission.objects.filter(discharge_date__isnull=True).select_related('patient__user', 'room', 'bed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_occupied_beds'] = Bed.objects.filter(status=False).count()
        context['discharges_today'] = Admission.objects.filter(
            discharge_date__date=timezone.now().date()
        ).count()
        return context

class AdmissionDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Admission
    template_name = 'hospital_facility/admission_detail.html'
    context_object_name = 'admission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admission = self.get_object()
        
        # Clinical Record Linkage: Filter by patient and date range of stay
        end_date = admission.discharge_date or timezone.now()
        
        context['medical_records'] = MedicalRecord.objects.filter(
            patient=admission.patient,
            record_date__range=(admission.admit_date, end_date)
        ).order_by('-record_date')
        
        context['lab_reports'] = LabReport.objects.filter(
            patient=admission.patient,
            report_date__range=(admission.admit_date, end_date)
        ).order_by('-report_date')
        
        # Billing Check
        context['unpaid_bills'] = admission.admission_bills.filter(status='UNPAID')
        context['is_cleared'] = not context['unpaid_bills'].exists()
        
        return context


class DischargePatientView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        admission = get_object_or_404(Admission, pk=pk)
        try:
            admission.status = 'DISCHARGED'
            admission.discharge_date = timezone.now()
            admission.save() # This triggers clean() and bed status update in models.py
            messages.success(request, f"Patient {admission.patient} has been successfully discharged.")
        except Exception as e:
            messages.error(request, f"Error during discharge: {str(e)}")
        
        return redirect('active_admission_list')

class RoomListView(LoginRequiredMixin, StaffRequiredMixin, ListView):

    model = Room
    template_name = 'hospital_facility/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        return Room.objects.all().prefetch_related('beds')

class RoomCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Room
    fields = ['dept', 'room_number', 'type', 'room_charge']
    template_name = 'hospital_facility/room_form.html'
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Room created successfully!')
        return super().form_valid(form)

class RoomUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Room
    fields = ['dept', 'room_number', 'type', 'room_charge']
    template_name = 'hospital_facility/room_form.html'
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Room updated successfully!')
        return super().form_valid(form)

class RoomDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Room
    template_name = 'hospital_facility/room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Room deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ToggleBedStatusView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, pk):
        bed = get_object_or_404(Bed, pk=pk)
        bed.status = not bed.status
        bed.save()
        status_str = "Available" if bed.status else "Occupied"
        messages.success(request, f'Bed {bed.bed_number} is now {status_str}.')
        return redirect('room_list')
