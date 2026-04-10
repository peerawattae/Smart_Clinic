from django.db import models
from django.conf import settings


class AppointmentQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.is_superuser:
            return self.all()
        if hasattr(user, 'role'):
            if user.role == 'doctor':
                return self.filter(doctor=user)
            if user.role == 'patient':
                return self.filter(patient=user)
        return self.none()

    def active(self):
        return self.filter(status__in=['pending', 'confirmed'])

    def history(self):
        return self.filter(status__in=['completed', 'cancelled', 'no_show'])


class AppointmentManager(models.Manager):
    def get_queryset(self):
        return AppointmentQuerySet(self.model, using=self._db)

    def for_user(self, user):
        return self.get_queryset().for_user(user)

    def active_for_user(self, user):
        return self.for_user(user).active()

    def history_for_user(self, user):
        return self.for_user(user).history()


class Appointment(models.Model):
    """A scheduled appointment between a patient and a doctor."""
    objects = AppointmentManager()


    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        NO_SHOW = 'no_show', 'No Show'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments',
        limit_choices_to={'role': 'patient'},
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_appointments',
        limit_choices_to={'role': 'doctor'},
    )
    date = models.DateField()
    time_slot = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    reason = models.TextField(
        blank=True,
        help_text='Reason for the appointment',
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes from staff',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder_sent = models.BooleanField(default=False)


    class Meta:
        ordering = ['-date', '-time_slot']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time_slot'],
                name='unique_doctor_slot',
            ),
        ]

    def __str__(self):
        return (
            f'Appointment: {self.patient.get_full_name()} with '
            f'Dr. {self.doctor.get_full_name()} on {self.date} at {self.time_slot}'
        )


class DoctorAvailability(models.Model):
    """Weekly recurring availability slots for doctors."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, 'Monday'
        TUESDAY = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY = 3, 'Thursday'
        FRIDAY = 4, 'Friday'
        SATURDAY = 5, 'Saturday'
        SUNDAY = 6, 'Sunday'

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availability_slots',
        limit_choices_to={'role': 'doctor'},
    )
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Doctor Availability'
        verbose_name_plural = 'Doctor Availabilities'
        ordering = ['weekday', 'start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'weekday', 'start_time'],
                name='unique_availability_slot',
            ),
        ]

    def __str__(self):
        return (
            f'Dr. {self.doctor.get_full_name()} — '
            f'{self.get_weekday_display()} {self.start_time}–{self.end_time}'
        )
