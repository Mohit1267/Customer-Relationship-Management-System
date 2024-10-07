'''from django.http import JsonResponse
from .models import MiningData
from datetime import datetime, timedelta
import os
import speech_recognition as sr

def speak_text(text):
    os.system(f'espeak "{text}"')

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak_text("I could not understand what you said.")
            return None
        except sr.RequestError as e:
            speak_text("There was an issue with the speech recognition service.")
            return None

def get_start_date(duration):
    today = datetime.now()
    
    if duration == "Todays":
        return today
    elif duration == "1 month":
        return today - timedelta(days=30)
    elif duration == "quarterly":
        return today - timedelta(days=90)
    elif duration == "yearly":
        return today - timedelta(days=365)
    else:
        return None

def mining_ct_voice_automated(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        speak_text("Please tell me if you want to search by zone, state, or district.")
        geo_field = recognize_speech()

        if geo_field:
            speak_text(f"Please provide the name of the {geo_field}.")
            geo_value = recognize_speech()

            speak_text("Please tell me the duration: Todays, 1 month, quarterly, or yearly.")
            duration = recognize_speech()

            if geo_value and duration:
                start_date = get_start_date(duration)

                if start_date:
                    filter_kwargs = {f"{geo_field}__iexact": geo_value, "date__gte": start_date}
                    mining_data = MiningData.objects.filter(**filter_kwargs)
                    mining_count = mining_data.count()

                    response = f"There are {mining_count} mining tasks in {geo_value} for the last {duration}."
                    speak_text(response)

                    return JsonResponse({'mining_count': mining_count, 'message': response})
                else:
                    speak_text("Invalid duration provided.")
                    return JsonResponse({'error': 'Invalid duration provided.'}, status=400)
            else:
                speak_text("No geographical value or duration was provided. Please try again.")
                return JsonResponse({'error': 'Geographical value or duration missing.'}, status=400)
        else:
            speak_text("No geographical field was provided. Please try again.")
            return JsonResponse({'error': 'Geographical field missing.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)'''
