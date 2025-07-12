import pyttsx3
import speech_recognition as sr
import subprocess
import webbrowser
import time
import random
import psutil
import os
import datetime
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from time import sleep
import sched
from googletrans import Translator

# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Initialize the translator
translator = Translator()

# Text-to-speech
def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Open program
def open_program(program_name):
    """Open a program based on the voice command."""
    if program_name.lower() == "notepad":
        speak("Opening Notepad.")
        subprocess.Popen("notepad.exe")  # Open Notepad
    elif program_name.lower() == "calculator":
        speak("Opening Calculator.")
        subprocess.Popen("calc.exe")  # Open Calculator
    elif program_name.lower() == "paint":
        speak("Opening Paint.")
        subprocess.Popen("mspaint.exe")  # Open Paint
    elif program_name.lower() == "word":
        speak("Opening Microsoft Word.")
        subprocess.Popen("winword.exe")  # Open Microsoft Word
    else:
        speak(f"Sorry, I cannot open {program_name} right now.")

# Open website
def open_website(website_name):
    """Open a website based on the voice command."""
    if website_name.lower() == "google":
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")  # Open Google
    elif website_name.lower() == "youtube":
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")  # Open YouTube
    elif website_name.lower() == "wikipedia":
        speak("Opening Wikipedia.")
        webbrowser.open("https://www.wikipedia.org")  # Open Wikipedia
    else:
        speak(f"Sorry, I cannot open {website_name} right now.")

# Get current time
def get_current_time():
    """Get the current time and speak it."""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")

# Tell a joke
def tell_joke():
    """random joke."""
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why did the scarecrow win an award? Because he was outstanding in his field.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t programmers like nature? It has too many bugs.",
        "How does a penguin build its house? Igloos it together!"
    ]
    speak(random.choice(jokes))

# Set a reminder
def set_reminder(task, reminder_time):
    """Set a reminder for a task."""
    speak(f"Setting a reminder for {task} at {reminder_time}.")
    
    # Convert reminder time to seconds
    reminder_time = datetime.strptime(reminder_time, "%H:%M")
    time_in_seconds = (reminder_time - datetime.now()).total_seconds()

    if time_in_seconds > 0:
        scheduler.enter(time_in_seconds, 1, remind_task, (task,))
        speak(f"Reminder for {task} set for {reminder_time.strftime('%H:%M')}")
    else:
        speak("The time you entered is in the past. Please enter a future time.")

# Reminder task
def remind_task(task):
    """Notify the user about the task reminder."""
    speak(f"Reminder: {task}")

# Get system info
def get_system_info():
    """Fetch and speak the system information."""
    speak("Fetching system information.")
    uname = subprocess.check_output("uname -a", shell=True).decode().strip()
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    speak(f"System Information: {uname}. CPU usage: {cpu}%. Memory usage: {memory}%.")
    
# Get battery status
def get_battery_status():
    """Fetch and speak the battery status."""
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = battery.power_plugged
    if plugged:
        speak(f"Your battery is currently at {percent} percent, and your charger is plugged in.")
    else:
        speak(f"Your battery is at {percent} percent, and it's not plugged in.")

# Send an email
def send_email(to_email, subject, body):
    """Send an email."""
    from_email = "your_email@gmail.com"
    password = "your_password"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Setup the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        speak("Email sent successfully.")
    except Exception as e:
        speak("Sorry, I was unable to send the email.")
        print("Error:", e)

# Translate text
def translate_text(text, dest_language='en'):
    """Translate text to the desired language."""
    try:
        translation = translator.translate(text, dest=dest_language)
        translated_text = translation.text
        speak(f"The translation is: {translated_text}")
    except Exception as e:
        speak("Sorry, I was unable to translate the text.")
        print("Translation Error:", e)

# Respond to commands
def respond_to_command(query):
    """Process the user's voice query and respond accordingly."""
    if "hello" in query.lower():
        speak("Hello, how can I assist you?")
        return True
    elif "exit" in query.lower():
        speak("Goodbye!")
        return False
    elif "translate" in query.lower():
        # Example: "Translate 'Hello' to Spanish"
        text_to_translate = query.split("translate")[-1].strip()
        if "to" in text_to_translate:
            text, lang = text_to_translate.rsplit(" to ", 1)
            dest_language = lang.strip().lower()
            translate_text(text, dest_language)
        else:
            speak("Please specify the language after 'to'. For example, 'Translate hello to Spanish'.")
        return True
    elif "open" in query.lower():
        program = query.split("open")[-1].strip()
        open_program(program)
        return True
    elif "what time is it" in query.lower():
        get_current_time()
        return True
    elif "tell me a joke" in query.lower():
        tell_joke()
        return True
    elif "set reminder" in query.lower():
        task_info = query.split("remind me to")[-1].strip()
        task, reminder_time = task_info.rsplit(" at ", 1)
        set_reminder(task, reminder_time)
        return True
    elif "system info" in query.lower():
        get_system_info()
        return True
    elif "battery status" in query.lower():
        get_battery_status()
        return True
    elif "send email" in query.lower():
        speak("Please say the recipient email address.")
        # Wait for the email address
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            to_email = recognizer.recognize_google(audio)
        
        speak("Please say the subject.")
        # Wait for the subject
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            subject = recognizer.recognize_google(audio)
        
        speak("Please say the body of the email.")
        # Wait for the body text
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            body = recognizer.recognize_google(audio)
        
        send_email(to_email, subject, body)
        return True
    else:
        speak(f"You said: {query}")
        return True

# Main voice assistant loop
def activate_voice_assistant():
    """Start the voice assistant, continuously listening for commands."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Starting Voice Assistant...")

    while True:
        try:
            print("Listening...")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Listen for speech

            query = recognizer.recognize_google(audio)  # Recognize speech
            print("You said:", query)
            speak(f"You said: {query}")

            if not respond_to_command(query):
                break

        except sr.UnknownValueError:
            speak("Hmm, are you there? I didn't hear anything.")
        except sr.WaitTimeoutError:
            speak("Hmm, are you there? I didn't hear anything.")
        except sr.RequestError as e:
            speak("Sorry, I can't reach the speech service right now.")
        except Exception as e:
            print("Error:", e)
            speak("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    activate_voice_assistant()
