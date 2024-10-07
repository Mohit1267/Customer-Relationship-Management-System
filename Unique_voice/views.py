'''from django.shortcuts import render

import datetime
import speech_recognition as sr
import subprocess  # To use espeak for Linux TTS
from .models import MiningData  # Adjust according to your Django project structure

# Function to convert text to speech using espeak (Linux)
def speak_text(text):
    subprocess.run(['espeak', text])

# Function to capture voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't catch that. Please try again.")
            return None

# Function to determine the start date based on the duration
def get_start_date(duration):
    now = datetime.datetime.now()
    if duration == "Todays":
        return now - datetime.timedelta(days=1)
    elif duration == "1 month":
        return now - datetime.timedelta(days=30)
    elif duration == "quarterly":
        return now - datetime.timedelta(days=90)
    elif duration == "yearly":
        return now - datetime.timedelta(days=365)
    else:
        return None

# Function to automate mining queries based on zone, state, district and duration
def mining_ct_voice_automated():
    # Step 1: Capture the user's voice for the geographical field (zone, state, district)
    speak_text("Please tell me if you want to search by zone, state, or district.")
    geo_field = recognize_speech()

    # Step 2: Capture the voice for the specific value of the chosen field (e.g., name of zone or state)
    if geo_field:
        speak_text(f"Please provide the name of the {geo_field}.")
        geo_value = recognize_speech()

        # Step 3: Capture the voice for the duration (Todays, 1 month, quarterly, or yearly)
        speak_text("Please tell me the duration: Todays, 1 month, quarterly, or yearly.")
        duration = recognize_speech()

        if geo_value and duration:
            # Get the start date based on the duration
            start_date = get_start_date(duration)

            if start_date:
                # Query the database based on the geo_field, geo_value, and date range
                filter_kwargs = {f"{geo_field}__iexact": geo_value, "date__gte": start_date}
                mining_data = MiningData.objects.filter(**filter_kwargs)

                mining_count = mining_data.count()

                # Step 4: Voice feedback
                response = f"There are {mining_count} mining tasks in {geo_value} for the last {duration}."
                print(response)
                speak_text(response)
                return mining_count
            else:
                speak_text("Invalid duration provided.")
                return None
        else:
            speak_text("No geographical value or duration was provided. Please try again.")
            return None
    else:
        speak_text("No geographical field was provided. Please try again.")
        return None

# Example call to the voice-automated function
mining_ct_voice_automated()'''




