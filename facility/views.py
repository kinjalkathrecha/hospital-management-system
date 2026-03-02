from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import (
    Room, Bed, Admission,
    Bill, Payment, Staff, StaffAssignment
)

from .serializers import (
    RoomSerializer, BedSerializer,
    AdmissionSerializer, BillSerializer,
    PaymentSerializer, StaffSerializer,
    StaffAssignmentSerializer
)


class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.select_related(
        'patient__user', 'doctor__user', 'room', 'bed'
    )
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Optional filter
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    @action(detail=True, methods=['post'])
    def discharge(self, request, pk=None):
        admission = self.get_object()

        if admission.status == 'DISCHARGED':
            return Response(
                {"error": "Already discharged"},
                status=status.HTTP_400_BAD_REQUEST
            )

        admission.status = 'DISCHARGED'
        admission.discharge_date = timezone.now()
        admission.save()

        return Response({"message": "Patient discharged successfully"})
    
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class BedViewSet(ModelViewSet):
    queryset = Bed.objects.select_related('room')
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.select_related('user')
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]

class StaffAssignmentViewSet(ModelViewSet):
    queryset = StaffAssignment.objects.select_related(
        'staff__user', 'patient__user'
    )
    serializer_class = StaffAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser or user.role == 'ADMIN':
            return super().get_queryset()

        return StaffAssignment.objects.filter(
            staff__user=user
        )
    
class BillViewSet(ModelViewSet):
    queryset = Bill.objects.select_related('patient__user')
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        bill = self.get_object()
        
        if bill.status == 'PAID':
            return Response({"message": "Bill is already paid."}, status=400)
            
        bill.status = 'PAID'
        bill.save()
        
        return Response({
            "message": "Bill marked as PAID",
            "total_collected": bill.total_amount
        })
    
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.select_related('bill')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]