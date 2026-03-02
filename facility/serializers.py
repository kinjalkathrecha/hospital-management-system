from rest_framework import serializers
from .models import Room, Bed, Admission, Bill, Payment, Staff, StaffAssignment
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from users.models import User
from users.serializers import UserSerializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Staff
        fields = ['id', 'user', 'salary', 'dept']

    def create(self, validated_data):
        from django.db import transaction
        user_data = validated_data.pop('user')
        
        with transaction.atomic():
            user = User.objects.create_user(**user_data, role='STAFF')
            staff = Staff.objects.create(user=user, **validated_data)
        return staff

class StaffAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAssignment
        fields = '__all__'
