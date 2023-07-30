import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator

def start_listening():
    global recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        try:
            audio = recognizer.listen(source, timeout=5)  # Record audio for 5 seconds
            print("Audio recording complete. Processing...")

            # Use the Google Web Speech API to recognize the speech
            text = recognizer.recognize_google(audio)

            # Update the label to show the transcribed text
            transcription_label.config(text=text)

            # Translate the text to a different language
            translated_text = translate_text(text, target_language="fr")  # Change "fr" to your desired target language code
            translation_label.config(text=translated_text)

        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

def save_to_file():
    # Get the transcribed text from the label
    transcribed_text = transcription_label.cget("text")

    # Save the transcribed text to a text file
    with open("transcribed_text.txt", "w") as file:
        file.write(transcribed_text)

    messagebox.showinfo("Save Successful", "Transcribed text saved to transcribed_text.txt")

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

# Create the tkinter application
app = tk.Tk()
app.title("Speech-to-Text and Translation")
app.geometry("500x500")

# Add UI elements
transcription_label = tk.Label(app, text="", wraplength=400, font=("Arial", 14))
transcription_label.pack(pady=20)

translation_label = tk.Label(app, text="", wraplength=400, font=("Arial", 14))
translation_label.pack(pady=20)

mic_button = tk.Button(app, text="Start Recording", command=start_listening, font=("Arial", 12))
mic_button.pack(pady=10)

save_button = tk.Button(app, text="Save", command=save_to_file, font=("Arial", 12))
save_button.pack(pady=10)

app.mainloop()
