# your_app/tasks.py

from datetime import timedelta
from django.utils import timezone
from users.models import AttendanceRecord, RegisterUser

def update_previous_day_attendance():
    current_date = timezone.localtime().date()
    previous_date = current_date - timedelta(days=1)

    users = RegisterUser.objects.all()
    for user in users:
        existing_record = AttendanceRecord.objects.filter(user=user, date=previous_date).first()
        if not existing_record:
            AttendanceRecord.objects.create(
                user=user,
                date=previous_date,
                status='Absent'
            )


# myapp/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import UserActivity
from datetime import timedelta

@shared_task
def check_user_activity():
    threshold_time = timezone.now() - timedelta(minutes=15)  # Set your threshold
    inactive_users = UserActivity.objects.filter(last_activity__lt=threshold_time)
    # Process inactive users as needed

