from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'experience', 'price')
    list_filter = ('specialization',)
    search_fields = ('full_name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient__username', 'doctor__full_name')