from rest_framework import serializers
from .models import Doctor, Appointment
from django.utils import timezone

class DoctorSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'experience', 'specialization', 'specialization_display', 'price']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.ReadOnlyField(source='patient.username')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date_time', 'status', 'created_at']

    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Нельзя записаться на прошедшее время.")
        return value