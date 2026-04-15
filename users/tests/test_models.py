from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification

User = get_user_model()

class UserProfileTests(TestCase):
    def test_doctor_profile_auto_creation(self):
        doctor = User.objects.create_user(
            username='drsmith',
            password='password123',
            role=User.Role.DOCTOR
        )
        self.assertTrue(hasattr(doctor, 'doctor_profile'))

    def test_patient_profile_auto_creation(self):
        patient = User.objects.create_user(
            username='jdoe',
            password='password123',
            role=User.Role.PATIENT
        )
        self.assertTrue(hasattr(patient, 'patient_profile'))

class NotificationModelTests(TestCase):
    def test_notification_str(self):
        user = User.objects.create_user(username='testuser')
        notif = Notification.objects.create(user=user, title="Hello", message="World")
        self.assertEqual(str(notif), f"Notification for {user.username}: Hello")
