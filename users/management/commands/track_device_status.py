# myapp/management/commands/track_device_status.py

import os
import time
import socket
import platform
from datetime import datetime
from django.core.management.base import BaseCommand
from users.models import UserActivity  # Adjust this import according to your app structure
from django.utils import timezone 

class Command(BaseCommand):
    help = 'Track device statuses and update uptime and downtime.'
    
    PASSIVE_TIME_LIMIT = 30  # 30 seconds

    def ping_device(self, ip):
        """ 
        Function to ping a device to check if it's active (online) or passive (offline).
        Returns True if the device is active, False otherwise.
        """
        # Use the appropriate command based on the operating system
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        response = os.system(f"ping {param} 1 {ip} > NUL 2>&1")
        return response == 0

    def handle(self, *args, **options):
        print("Starting to track devices' statuses...\n")
        
        # Ensure local device IP is added to the DeviceActivity table
        local_ip = socket.gethostbyname(socket.gethostname())
        UserActivity.objects.get_or_create(ip_address=local_ip)

        while True:
            current_time = timezone.now()
            devices = UserActivity.objects.all()  # Fetch all devices from the database
            
            for device in devices:
                is_active = self.ping_device(device.ip_address)

                if is_active:
                    if device.is_active != 'active':
                        device.uptime = (current_time - device.last_check).total_seconds() if device.last_check else 0
                        device.downtime = None  # Reset downtime
                        device.last_check = current_time
                        device.is_active = 'active'
                        device.last_status_change = current_time
                        device.save()  # Save changes to the database
                        print(f"[{device.ip_address}] Device is now ACTIVE. Uptime started at {device.last_check}")
                else:
                    if device.last_check is None or (current_time - device.last_check).total_seconds() > self.PASSIVE_TIME_LIMIT:
                        if device.is_active != 'passive':
                            device.downtime = (current_time - device.last_check).total_seconds() if device.last_check else 0
                            device.uptime = None  # Reset uptime
                            device.last_check = current_time
                            device.is_active = 'passive'
                            device.last_status_change = current_time
                            device.save()  # Save changes to the database
                            print(f"[{device.ip_address}] Device is now PASSIVE. Downtime started at {device.last_check}")

            # Optional: Sleep before the next status report
            time.sleep(10)  # Adjust time as needed
