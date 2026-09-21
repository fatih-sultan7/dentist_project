from django.contrib.auth.models import User
from django.db import models

class Doctor(models.Model):
    DENTAL_SPECIALIZATIONS = (
        ('therapist', 'Стоматолог-терапевт'),
        ('surgeon', 'Стоматолог-хирург'),
        ('orthodontist', 'Ортодонт'),
        ('orthopedist', 'Ортопед'),
        ('implantologist', 'Имплантолог'),
        ('pediatric', 'Детский стоматолог'),
    )

    full_name = models.CharField(max_length=255, verbose_name="ФИО врача")
    experience = models.PositiveIntegerField(verbose_name="Опыт (лет)")
    specialization = models.CharField(max_length=50, choices=DENTAL_SPECIALIZATIONS, verbose_name="Направление")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Стоимость приема")

    def __str__(self):
        return f"{self.full_name} ({self.get_specialization_display()})"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
    )
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пациент")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    date_time = models.DateTimeField(verbose_name="Дата и время приема")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Пациент {self.patient.username} у врача {self.doctor.full_name}"