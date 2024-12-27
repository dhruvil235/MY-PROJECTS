import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import subprocess
import datetime
import tkinter as tk
from tkinter import Text, Scrollbar
import pyautogui
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def listen(lang="hindi"):
    """Capture voice input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'DHRUVIL sir '...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language=lang)
            print(f"Dhruvil said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

def wait_for_wake_word():
    """Wait until the wake word 'DHRUVIL' is heard."""
    while True:
        command = listen()
        if "jp" in command:
            speak(" Dhru-vil sir,command mode activated")
            append_output(" Dhru-vil sir,command mode activated")
            return

def open_application(app_name):
    """Open specified application."""
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "spotify": "C:\\Users\\YourUsername\\AppData\\Roaming\\Spotify\\Spotify.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
        "whatsapp":"whatsapp.exe"
    }

    if app_name in app_paths:
        app_path = app_paths[app_name]
        speak(f"Opening {app_name}.")
        append_output(f"Opening {app_name}.")
        subprocess.Popen(app_path)
    else:
        speak("Sorry, I don't know how to open that application.")
        append_output("Sorry, I don't know how to open that application.")

def execute_command(command):
    """Perform tasks based on the user's command."""
    if "open browser" in command:
        speak("Opening the browser.")
        append_output("Opening the browser.")
        webbrowser.open("http://www.google.com")
    elif "play music" in command:
        music_folder = "C:\\Users\\YourUsername\\Music"
        os.startfile(music_folder)
        speak("Playing your music.")
        append_output("Playing your music.")
    elif "what time is it" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}.")
        append_output(f"The time is {time_now}.")
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        speak(f"Searching for {search_query}.")
        append_output(f"Searching for {search_query}.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif "shutdown" in command:
        speak("Shutting down the system. Goodbye!")
        append_output("Shutting down the system.")
        subprocess.call("shutdown /s /t 1", shell=True)
    elif "write" in command:
        note = command.replace("write", "").strip()
        with open("JarvisNotes.txt", "a") as file:
            file.write(f"{note}\n")
        speak("Note saved.")
        append_output("Note saved.")
    elif "open" in command:
        # Extract application name from the command
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    else:
        speak("I'm not sure what you mean.")
        append_output("I'm not sure what you mean.")

def handle_command():
    """Get input from the text box and execute it."""
    command = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)
    if command:
        append_output(f"You: {command}")
        execute_command(command)

def start_voice_mode():
    """Run the assistant in voice mode."""
    def listen_and_execute():
        while True:
            command = listen()
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                append_output("Goodbye!")
                break
            execute_command(command)

    threading.Thread(target=listen_and_execute, daemon=True).start()

def append_output(text):
    """Display output in the GUI."""
    output_box.insert(tk.END, f"{text}\n")
    output_box.see(tk.END)

# GUI setup
app = tk.Tk()
app.title("Dhruvil's Assistant")
app.geometry("600x400")

# Text display for output
output_box = Text(app, wrap="word", height=15, width=70)
output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Scrollbar for output
scrollbar = Scrollbar(output_box)
output_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Input box for commands
input_box = tk.Text(app, height=2, width=70)
input_box.pack(padx=10, pady=5, fill=tk.BOTH)

# Buttons for actions
button_frame = tk.Frame(app)
button_frame.pack(pady=5)

execute_button = tk.Button(button_frame, text="Execute", command=handle_command)
execute_button.grid(row=0, column=0, padx=5)

voice_mode_button = tk.Button(button_frame, text="Voice Mode", command=start_voice_mode)
voice_mode_button.grid(row=0, column=1, padx=5)

exit_button = tk.Button(button_frame, text="Exit", command=app.quit)
exit_button.grid(row=0, column=2, padx=5)

# # Start GUI loop
# speak("Hello, I am dhru-vil, your personal assistant.")
# speak("say , jp to command mode activate.")
# append_output("Hello, I am dhru-vil, your personal assistant.")
# append_output("say , jp to command mode activate.")
wait_for_wake_word()  # Start listening for the wake word

# Start the Tkinter event loop
app.mainloop()
