import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    print("You said: " + recognizer.recognize_google(audio))
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service.")
