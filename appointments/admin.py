from django.contrib import admin

from .models import Appointment, DoctorAvailability


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time_slot', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = (
        'patient__first_name', 'patient__last_name',
        'doctor__first_name', 'doctor__last_name',
    )
    date_hierarchy = 'date'


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'weekday', 'start_time', 'end_time', 'is_active')
    list_filter = ('weekday', 'is_active', 'doctor')
