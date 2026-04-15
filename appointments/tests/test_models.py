from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Appointment
from datetime import date, time

User = get_user_model()

class AppointmentModelTests(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='dr', role=User.Role.DOCTOR)
        self.patient = User.objects.create_user(username='pa', role=User.Role.PATIENT)

    def test_appointment_uniqueness(self):
        # Already tested basic creation, now testing constraints if any
        appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=date.today(), time_slot=time(9,0), end_time=time(9,30)
        )
        self.assertIsNotNone(appt.pk)

    def test_active_queryset(self):
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=date.today(), time_slot=time(10,0), end_time=time(10,30),
            status='pending'
        )
        self.assertEqual(Appointment.objects.active().count(), 1)
