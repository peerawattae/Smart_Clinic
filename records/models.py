from django.db import models
from django.conf import settings


class MedicalRecordManager(models.Manager):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if hasattr(user, 'role'):
            if user.role == 'doctor':
                return self.filter(doctor=user)
            if user.role == 'patient':
                return self.filter(patient=user)
        return self.none()


class MedicalRecord(models.Model):
    """A medical record created during or after an appointment."""
    objects = MedicalRecordManager()


    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='medical_records',
        limit_choices_to={'role': 'patient'},
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored_records',
        limit_choices_to={'role': 'doctor'},
    )
    appointment = models.ForeignKey(
        'appointments.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medical_records',
    )
    diagnosis = models.TextField()
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'Record #{self.pk} — {self.patient.get_full_name()} '
            f'({self.created_at:%Y-%m-%d})'
        )


class Prescription(models.Model):
    """A prescription linked to a medical record."""

    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='prescriptions',
    )
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(
        max_length=100,
        help_text='e.g. "Twice daily", "Every 8 hours"',
    )
    duration = models.CharField(
        max_length=100,
        help_text='e.g. "7 days", "2 weeks"',
    )
    instructions = models.TextField(
        blank=True,
        help_text='Special instructions for the patient',
    )

    def __str__(self):
        return f'{self.medication_name} — {self.dosage} ({self.frequency})'


class VitalSign(models.Model):
    """Vital signs recorded during a visit."""

    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='vital_signs',
    )
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True,
        help_text='Body temperature in °C',
    )
    blood_pressure_systolic = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Systolic blood pressure (mmHg)',
    )
    blood_pressure_diastolic = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Diastolic blood pressure (mmHg)',
    )
    heart_rate = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Heart rate (bpm)',
    )
    respiratory_rate = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Respiratory rate (breaths/min)',
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text='Weight in kg',
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text='Height in cm',
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f'Vitals for Record #{self.record_id} ({self.recorded_at:%Y-%m-%d %H:%M})'


class MedicalRecordAccessRequest(models.Model):
    """A request from a patient to view their full medical record."""
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='access_requests')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('record', 'patient')

    def __str__(self):
        return f'Access Request: {self.patient.username} for Record #{self.record.id} ({self.status})'
