from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Room, Bed

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['STAFF', 'ADMIN']
    
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
