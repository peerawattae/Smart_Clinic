from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from users.models import Notification

@receiver(post_save, sender=Appointment)
def notify_appointment_changes(sender, instance, created, **kwargs):
    if created:
        # 1. Notify user when they book new booking
        Notification.objects.create(
            user=instance.patient,
            title="Appointment Booked",
            message=f"Your appointment with Dr. {instance.doctor.get_full_name()} on {instance.date} has been successfully booked. Status is currently: {instance.get_status_display()}."
        )

        # 2. Notify doctor about new booking
        Notification.objects.create(
            user=instance.doctor,
            title="New Patient Booking",
            message=f"You have a new appointment booking from {instance.patient.get_full_name()} for {instance.date} at {instance.time_slot.strftime('%I:%M %p')}."
        )

    else:
        # 2. Notify when status change from pending to confirm (or ANY status update that benefits user)
        if hasattr(instance, '_original_status') and instance.status != instance._original_status:
            title = "Appointment Status Updated"
            message = f"Your appointment with Dr. {instance.doctor.get_full_name()} on {instance.date} status has changed to: {instance.get_status_display()}."
            
            if instance.status == 'confirmed':
                title = "Appointment Confirmed!"
                message = f"Great news! Dr. {instance.doctor.get_full_name()} has confirmed your appointment for {instance.date} at {instance.time_slot.strftime('%I:%M %p')}."
            elif instance.status == 'cancelled':
                title = "Appointment Cancelled"
                message = f"We're sorry, your appointment with Dr. {instance.doctor.get_full_name()} on {instance.date} has been cancelled."
            
            Notification.objects.create(
                user=instance.patient,
                title=title,
                message=message
            )
