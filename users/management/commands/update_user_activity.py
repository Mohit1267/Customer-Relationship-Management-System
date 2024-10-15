from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import UserActivity
from datetime import timedelta

class Command(BaseCommand):
    help = "Updates uptime and downtime for users"

    def handle(self, *args, **options):
        # Get the current time
        current_time = timezone.now()
        
        # Define the time interval (e.g., 10 minutes)
        time_interval = timedelta(minutes=10)
        
        # Loop through all user activities
        for user_activity in UserActivity.objects.all():
            last_activity = user_activity.last_activity

            # Calculate uptime (time since last activity)
            if last_activity + time_interval <= current_time:
                # Increment uptime if user is active
                user_activity.total_uptime += time_interval
            else:
                # Increment downtime if user is inactive
                user_activity.total_downtime += time_interval
            
            # Update last activity time
            user_activity.last_activity = current_time
            user_activity.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated user activity'))