from django.test import TestCase
from django.utils import timezone
from users.models import User
from appointments.models import Appointment
from records.models import MedicalRecord, Prescription, MedicalRecordAccessRequest

class MedicalRecordModelTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(username='drsmith', role='doctor')
        self.patient = User.objects.create_user(username='johndoe', role='patient')
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=timezone.now().date(),
            time_slot=timezone.now().time(),
            end_time=(timezone.now() + timezone.timedelta(hours=1)).time(),
            reason='Checkup'
        )
        self.record = MedicalRecord.objects.create(
            appointment=self.appointment,
            patient=self.patient,
            doctor=self.doctor,
            diagnosis='Common Cold'
        )

    def test_record_creation(self):
        self.assertEqual(self.record.patient, self.patient)
        self.assertEqual(self.record.diagnosis, 'Common Cold')

    def test_prescription_link(self):
        Prescription.objects.create(
            record=self.record,
            medication_name='Vitamin C',
            dosage='500mg'
        )
        self.assertEqual(self.record.prescriptions.count(), 1)

    def test_access_request_creation(self):
        request = MedicalRecordAccessRequest.objects.create(
            record=self.record,
            patient=self.patient
        )
        self.assertEqual(request.status, 'pending')
