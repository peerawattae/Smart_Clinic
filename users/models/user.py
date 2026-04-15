from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def doctors(self):
        return self.filter(role='doctor')

    def patients(self):
        return self.filter(role='patient')

class User(AbstractUser):
    """Custom user model with role-based access for the clinic."""
    objects = UserManager()

    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'
        NURSE = 'nurse', 'Nurse'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PATIENT,
    )
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
