from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from users.models import User, Notification
from appointments.models import Appointment
from records.models import MedicalRecord, MedicalRecordAccessRequest

class MedicalRecordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = User.objects.create_user(username='drsmith', role='doctor')
        self.patient = User.objects.create_user(username='johndoe', role='patient')
        self.other_patient = User.objects.create_user(username='janedoe', role='patient')
        
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=timezone.now().date(),
            time_slot=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            status='confirmed'
        )
        self.record = MedicalRecord.objects.create(
            appointment=self.appointment,
            patient=self.patient,
            doctor=self.doctor,
            diagnosis='Private Info'
        )

    def test_doctor_can_view_record(self):
        self.client.force_login(self.doctor)
        response = self.client.get(reverse('records:record_detail', kwargs={'pk': self.record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Info')

    def test_patient_restricted_view(self):
        self.client.force_login(self.patient)
        response = self.client.get(reverse('records:record_detail', kwargs={'pk': self.record.id}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Private Info')
        self.assertContains(response, 'Full Record Locked')

    def test_request_access_workflow(self):
        self.client.force_login(self.patient)
        # 1. Request access
        response = self.client.post(reverse('records:request_access', kwargs={'record_id': self.record.id}))
        self.assertEqual(MedicalRecordAccessRequest.objects.count(), 1)
        
        # 2. Doctor approves
        access_req = MedicalRecordAccessRequest.objects.first()
        self.client.force_login(self.doctor)
        self.client.post(reverse('records:approve_access', kwargs={'request_id': access_req.id}), {'action': 'approve'})
        
        # 3. Patient can now see info
        self.client.force_login(self.patient)
        response = self.client.get(reverse('records:record_detail', kwargs={'pk': self.record.id}))
        self.assertContains(response, 'Private Info')
        self.assertNotContains(response, 'Full Record Locked')
