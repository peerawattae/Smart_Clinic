from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Appointment
from datetime import date, time

User = get_user_model()

class AppointmentAPITests(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='dr2', role=User.Role.DOCTOR)
        self.patient = User.objects.create_user(username='pa2', role=User.Role.PATIENT)
        self.appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=date(2026, 4, 16), time_slot=time(9, 0), end_time=time(9, 30),
            status='confirmed'
        )

    def test_get_taken_slots_api(self):
        url = reverse('appointments:get_taken_slots')
        response = self.client.get(url, {'doctor_id': self.doctor.id, 'date': '2026-04-16'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('09:00', data['taken_slots'])

    def test_get_taken_slots_empty(self):
        url = reverse('appointments:get_taken_slots')
        response = self.client.get(url, {'doctor_id': self.doctor.id, 'date': '2026-04-17'})
        self.assertEqual(response.json()['taken_slots'], [])
