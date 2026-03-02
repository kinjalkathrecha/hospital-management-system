from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.db import transaction
from rest_framework import serializers
from .models import User, Doctor, Patient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'DOCTOR'
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor
    
    
class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'gender', 'age', 'phone', 
            'emergency_number', 'birth_date', 'blood_group', 
            'address', 'city', 'created_date'
        ]

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'PATIENT'
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient