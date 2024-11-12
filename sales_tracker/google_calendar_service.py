'''import os
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Set up base directory
BASE_DIR = '/home/admin1/Desktop/shanaya_cc/Sales_Tracker_Shanaya_Team/sales_tracker'

# Path to the credentials file
CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, 'client_secret', 'client_secret', 'service_account.json')

# Check if the file exists
print("Credentials file exists:", os.path.exists(CREDENTIALS_FILE_PATH))


# Specify the scopes for calendar access
scopes = ['https://www.googleapis.com/auth/calendar.events']

# Initiate the OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE_PATH, scopes=scopes)
credentials = flow.run_local_server(port=0)

# Create a Google Calendar API service
service = build('calendar', 'v3', credentials=credentials)

# Function to create a Google Meet event
def create_meeting_event(start_time, duration):
    # Define event details
    event = {
        'summary': 'Meeting Invitation',
        'description': 'Google Meet meeting invitation from uniquebaba',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (start_time + timedelta(minutes=duration)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
       
        'conferenceData': {
            'createRequest': {
                'requestId': 'meeting1234',  # Use any unique ID
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            }
        },
    }

    # Insert the event into the calendar
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return event.get('hangoutLink')

# Example usage
if __name__ == "__main__":
    # Define event details
    start_time = datetime.now() + timedelta(days=1)  # Schedule for 1 day from now
    duration = 60  # Event duration in minutes
    #attendees_emails = ['attendee@example.com']

    # Create the event and get the Google Meet link
    meet_link = create_meeting_event(start_time, duration)
    print("Google Meet link:", meet_link)'''


'''
import os
import json
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up base directory
BASE_DIR = '/home/admin1/Desktop/shanaya_cc/Sales_Tracker_Shanaya_Team/sales_tracker'

# Path to the credentials file
CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, 'client_secret', 'client_secret', 'service_account.json')

# Dummy credentials
dummy_credentials = {
    "installed": {
        "client_id": "your_client_id_here",
        "project_id": "your_project_id_here",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "your_client_secret_here",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

# Check if the credentials file exists
try:
    if not os.path.exists(CREDENTIALS_FILE_PATH):
        print("Credentials file does not exist. Creating a dummy file.")
        with open(CREDENTIALS_FILE_PATH, 'w') as json_file:
            json.dump(dummy_credentials, json_file, indent=4)
    else:
        print("Credentials file exists:", CREDENTIALS_FILE_PATH)

    # Specify the scopes for calendar access
    scopes = ['https://www.googleapis.com/auth/calendar.events']

    # Initiate the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE_PATH, scopes=scopes)
    credentials = flow.run_local_server(port=0)

    # Create a Google Calendar API service
    service = build('calendar', 'v3', credentials=credentials)

    # Function to create a Google Meet event
    def create_meeting_event(start_time, duration, attendees_emails):
        # Define event details
        event = {
            'summary': 'Meeting Invitation',
            'description': 'Google Meet meeting invitation from uniquebaba',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': (start_time + timedelta(minutes=duration)).isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [{'email': email} for email in attendees_emails],
            'conferenceData': {
                'createRequest': {
                    'requestId': 'meeting1234',  # Use any unique ID
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                }
            },
        }

        # Insert the event into the calendar
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        return event.get('hangoutLink')

    # Example usage
    if __name__ == "__main__":
        # Define event details
        start_time = datetime.now() + timedelta(days=1)  # Schedule for 1 day from now
        duration = 60  # Event duration in minutes
        attendees_emails = ['attendee@example.com']

        # Create the event and get the Google Meet link
        meet_link = create_meeting_event(start_time, duration, attendees_emails)
        print("Google Meet link:", meet_link)

except Exception as e:
    print(f"An error occurred: {e}")'''
