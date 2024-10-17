# myapp/management/commands/check_device_status.py

from django.core.management.base import BaseCommand
from users.models import UserActivity
from users.utils import check_device_status

class Command(BaseCommand):
    help = 'Check device activity status'

    def handle(self, *args, **kwargs):
        devices = UserActivity.objects.all()
        for device in devices:
            check_device_status(device)
        self.stdout.write(self.style.SUCCESS('Device statuses updated'))