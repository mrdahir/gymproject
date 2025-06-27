from django.core.management.base import BaseCommand
from django.utils import timezone
from members.models import Member
from datetime import timedelta

def send_notification(member):
    # Placeholder: integrate with email/SMS
    print(f"Alert: Member {member} expires in {member.days_until_expiry()} days.")

class Command(BaseCommand):
    help = 'Check for memberships expiring in 3 days'

    def handle(self, *args, **options):
        today = timezone.now().date()
        alert_date = today + timedelta(days=3)
        for member in Member.objects.all():
            if member.expiry_date == alert_date:
                send_notification(member)
        self.stdout.write(self.style.SUCCESS('Expiry check complete.')) 