# users/management/commands/populate_device_activity.py
from django.core.management.base import BaseCommand
from users.models import UserActivity  # Adjust the import according to your app structure

class Command(BaseCommand):
    help = 'Populate Device Activity'

    def handle(self, *args, **kwargs):
        # Example of adding device IPs
        device_ips = [
            "192.168.29.187",  # Replace with actual IPs
            "192.168.1.3",
            "192.168.1.4",
        ]

        for ip in device_ips:
            # Specify the user_id you want to associate with these device activities
            user_id = 1  # Replace with an appropriate user ID from your User model
            UserActivity.objects.get_or_create(ip_address=ip, user_id=user_id)

        self.stdout.write(self.style.SUCCESS("Device IPs have been populated in the database."))
