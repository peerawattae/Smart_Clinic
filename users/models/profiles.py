from django.db import models
from .user import User

class DoctorProfile(models.Model):
    """Extended profile for users with the Doctor role."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        limit_choices_to={'role': User.Role.DOCTOR},
    )
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctor Profiles'

    def __str__(self):
        return f'Dr. {self.user.get_full_name()} — {self.specialization}'

class PatientProfile(models.Model):
    """Extended profile for users with the Patient role."""
    class BloodType(models.TextChoices):
        A_POS = 'A+', 'A+'
        A_NEG = 'A-', 'A-'
        B_POS = 'B+', 'B+'
        B_NEG = 'B-', 'B-'
        AB_POS = 'AB+', 'AB+'
        AB_NEG = 'AB-', 'AB-'
        O_POS = 'O+', 'O+'
        O_NEG = 'O-', 'O-'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        limit_choices_to={'role': User.Role.PATIENT},
    )
    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices,
        blank=True,
    )
    allergies = models.TextField(blank=True, help_text='Known allergies')
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patient Profiles'

    def __str__(self):
        return f'Patient: {self.user.get_full_name()}'
