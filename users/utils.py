# myapp/utils.py

import subprocess
from datetime import datetime
from django.utils import timezone  # Import the timezone module

def ping_device(ip_address):
    try:
        response = subprocess.run(
            ["ping", "-c", "1", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return response.returncode == 0
    except Exception as e:
        print(f"Error pinging device: {e}")
        return False

def check_device_status(device):
    now = timezone.now()
    is_active = ping_device(device.ip_address)
    
    if is_active:
        device.total_uptime += now - device.last_check
        device.is_active = True
    else:
        device.total_downtime += now - device.last_check
        device.is_active = False

    device.last_check = now
    device.save()
