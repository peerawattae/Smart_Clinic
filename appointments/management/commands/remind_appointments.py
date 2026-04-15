from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from ...models import Appointment
from users.models import Notification

class Command(BaseCommand):
    help = 'Sends reminders to patients 24 hours before their appointments'

    def handle(self, *args, **options):
        now = timezone.now()
        # Target end date is tomorrow
        end_date = now.date() + timedelta(days=1)
        
        # Get pending/confirmed appointments for today or tomorrow that haven't had reminders sent
        appointments = Appointment.objects.filter(
            date__range=[now.date(), end_date],
            status__in=['pending', 'confirmed'],
            reminder_sent=False
        )


        count = 0
        for appt in appointments:
            # 1. Create In-app notification
            Notification.objects.create(
                user=appt.patient,
                title="Appointment Reminder",
                message=f"Reminder: You have an appointment with Dr. {appt.doctor.get_full_name()} tomorrow at {appt.time_slot.strftime('%I:%M %p')}."
            )

            # 2. Send Email
            subject = f"Reminder: Your Appointment with Smart Clinic - Tomorrow"
            message = (
                f"Dear {appt.patient.get_full_name()},\n\n"
                f"This is a reminder for your upcoming appointment:\n"
                f"Doctor: Dr. {appt.doctor.get_full_name()}\n"
                f"Date: {appt.date}\n"
                f"Time: {appt.time_slot.strftime('%I:%M %p')}\n\n"
                f"Please let us know if you need to reschedule."
            )
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [appt.patient.email],
                    fail_silently=False,
                )
                
                # Mark as sent
                appt.reminder_sent = True
                appt.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder for appt {appt.id}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to send email for appt {appt.id}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Total reminders sent: {count}'))
