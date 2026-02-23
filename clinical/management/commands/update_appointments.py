from django.core.management.base import BaseCommand
from django.utils import timezone
from clinical.models import Appointment

class Command(BaseCommand):
    help = 'Updates the status of appointments that have passed their scheduled time.'

    def handle(self, *args, **options):
        now = timezone.now()
        
        # We only care about PENDING or APPROVED appointments that are in the past
        overdue_appointments = Appointment.objects.filter(
            appointment_date__lt=now,
            status__in=['PENDING', 'APPROVED']
        )
        
        count = overdue_appointments.count()
        success_count = 0
        
        for appointment in overdue_appointments:
            if appointment.update_overdue_status():
                success_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {success_count} appointments out of {count} overdue.')
        )
