from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment, LabReport, Department, MedicalRecord
from .serializers import (
    AppointmentSerializer,
    LabReportSerializer,
    DepartmentSerializer,
    MedicalRecordSerializer
)
from permissions import IsPatient, IsDoctor, IsAdmin, IsStaffOrDoctor

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsPatient()]
        elif self.action in ['update_status']:
            return [IsDoctor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)

    @action(detail=True, methods=['patch'], permission_classes=[IsDoctor])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        status_value = request.data.get('status')

        if status_value in ['APPROVED', 'COMPLETED', 'CANCELLED']:
            appointment.status = status_value
            appointment.save()
            return Response({'message': 'Status updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class LabReportViewSet(ModelViewSet):
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsStaffOrDoctor()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return LabReport.objects.filter(patient=user.patient_profile)
        return LabReport.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role == 'DOCTOR':
            serializer.save(doctor=self.request.user.doctor_profile)
        else:
            serializer.save()

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdmin]

class MedicalRecordViewSet(ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsDoctor()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return MedicalRecord.objects.filter(patient=user.patient_profile)
        return MedicalRecord.objects.all()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor_profile)