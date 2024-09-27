# stpa/Users/management/commands/update_attendance.py

from django.core.management.base import BaseCommand
from users.tasks import update_previous_day_attendance

class Command(BaseCommand):
    help = 'Update previous day attendance'

    def handle(self, *args, **kwargs):
        update_previous_day_attendance()
        self.stdout.write(self.style.SUCCESS('Successfully updated previous day attendance'))
