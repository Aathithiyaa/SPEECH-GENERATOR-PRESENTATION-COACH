import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone as the audio source
with sr.Microphone() as source:
    print("Please speak something...")
    # Adjust for ambient noise and record the speech
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

# Recognize speech using Google's speech recognition service
try:
    print("You said: " + recognizer.recognize_google(audio))
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
