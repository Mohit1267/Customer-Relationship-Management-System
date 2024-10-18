from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from datetime import datetime, time, timedelta
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone



# Create your models here.

class RegisterUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('miner', 'Data Miner'),
        ('agent', 'Calling Agent'),
        ('sales', 'Sales Agent'),
    )
    user = models.OneToOneField(RegisterUser, on_delete=models.CASCADE, default= get_user_model(), primary_key=True)
    emp_id = models.CharField(max_length=50,default="qw")
    dob = models.DateField()
    branch = models.CharField(max_length=10, choices=USER_ROLES)
    can_login = models.BooleanField(default=True)
    can_logout = models.BooleanField(default=False)
    voice_sample = models.FileField(upload_to='voice_samples/', blank=True, null=True)


    def __str__(self):
        return self.user.username
    

class AttendanceRecord(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    # bw_login = models.TimeField(null=True, blank=True)
    # downtime = models.DurationField(default=timedelta(0), null = True, blank = True)
    # uptime = models.DurationField(default=timedelta(0), null = True, blank = True)
    status = models.CharField(
        max_length=20,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')],
        default='Absent'  # Default to 'Absent' for existing records
    )

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.status}"



class UpdownTime(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    downtime = models.DurationField(default=timedelta(0), null = True, blank = True)
    uptime = models.DurationField(default=timedelta(0), null = True, blank = True)

    # def save(self,*args, **kwargs):
    #     if self.check_in_time and self.check_out_time:
    #         check_in_datetime = datetime.combine(self.date, self.check_in_time)
    #         check_out_datetime = datetime.combine(self.date, self.check_out_time)
    #         self.uptime = check_out_datetime - check_in_datetime

# login : 9
# logout : 9:30
# uptime = logout-login
# login again = 10
# downtime : login - logout

class DaysStatus(models.Model):
    STATUS_CHOICES = (
        ('Holiday', 'Holiday'),
        ('Working Day', 'Working Day'),
    )
    date = models.DateField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.date} - {self.status}"





    
class CallingDetail(models.Model):
    caller = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default= get_user_model())
    customer_first_name = models.CharField(max_length=50, default="")
    customer_last_name = models.CharField(max_length=50, default= "")
    customer_email = models.EmailField(default="@gmail.com", unique=True)
    customer_contact_number = models.IntegerField(default=91)
    customer_address = models.TextField(default="")




class UserActivity(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    last_activity = models.DateTimeField(auto_now=True)
    total_uptime = models.DurationField(default=timedelta)  # Stores total uptime duration
    total_downtime = models.DurationField(default=timedelta) 
    last_check = models.DateTimeField(auto_now=True)
    is_active = models.CharField(max_length=10, default='unknown')
    class Meta:
        unique_together = ('user', 'ip_address')  # Ensure unique combination of user and IP address

    def __str__(self):
        return f"{self.user.email} - {self.ip_address} - {self.last_activity}"

# request.user = emailid
# request.user.usrname = username
# request.user.email = emailid'
# request.user.id = userid




class Location(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    temp = models.CharField(max_length=255, null = True)


    def __str__(self):
        return f"{self.profile.user.username} at {self.date} {self.time}"
    

