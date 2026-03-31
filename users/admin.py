from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, DoctorProfile, PatientProfile


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Clinic Info', {'fields': ('role', 'phone', 'date_of_birth', 'address', 'profile_image')}),
    )

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.role == User.Role.DOCTOR:
            return [DoctorProfileInline]
        if obj.role == User.Role.PATIENT:
            return [PatientProfileInline]
        return []


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'years_of_experience')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'insurance_provider')
    search_fields = ('user__first_name', 'user__last_name')
