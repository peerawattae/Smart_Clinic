from django.contrib import admin

from .models import MedicalRecord, Prescription, VitalSign


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1


class VitalSignInline(admin.StackedInline):
    model = VitalSign
    extra = 0


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = (
        'patient__first_name', 'patient__last_name',
        'diagnosis',
    )
    date_hierarchy = 'created_at'
    inlines = [PrescriptionInline, VitalSignInline]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'dosage', 'frequency', 'duration', 'record')
    search_fields = ('medication_name',)


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('record', 'temperature', 'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'recorded_at')
