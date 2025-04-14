import os
os.environ["TRANSFORMERS_NO_TF"] = "1"  # 👈 Force Transformers to ignore TensorFlow
import speech_recognition as sr
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tokenize import sent_tokenize

import nltk
nltk.download('punkt_tab')



sentiment_pipeline = pipeline("sentiment-analysis")


recognizer = sr.Recognizer()

def get_user_input():
    print("🎙️ How would you like to give your speech?")
    print("1. Voice Input")
    print("2. Text Input")
    choice = input("Enter 1 or 2: ").strip()
    return choice

import speech_recognition as sr

def get_text_from_voice():
    recognizer = sr.Recognizer()  # Initialize recognizer inside the function
    
    with sr.Microphone() as source:
        print("🎤 Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        recognizer.pause_threshold=1.5 # Adjust for ambient noise
        print("🎤 Speak now...")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=30)  # Wait for up to 10 seconds for speech
            print("🎤 Listening...")

            # Recognize speech using Google's speech recognition service
            text = recognizer.recognize_google(audio)
            print("\n📝 Transcription: ", text)
            return text

        except sr.WaitTimeoutError:
            print("⚠️ Timeout reached. No speech detected.")
            return "No speech detected."
        except sr.UnknownValueError:
            print("⚠️ Speech not recognized.")
            return "Speech not recognized."
        except sr.RequestError as e:
            print(f"⚠️ API error: {e}")
            return f"API error: {e}"



def get_text_from_input():
    print("📝 Enter your speech below:")
    return input(">> ")

def analyze_sentiment(text):
    result = sentiment_pipeline(text, truncation=True, padding=True, max_length=512)[0]
    label = result['label']
    confidence = result['score']
    return label, confidence

def structure_score(text):
    sentences = sent_tokenize(text)
    score = min(100, len(sentences) * 10) 
    return round(score, 2), len(sentences)

def suggest_improvements(label, confidence, sentence_count):
    suggestions = []
    if confidence < 60:
        suggestions.append("Try to sound more confident and assertive.")
    if sentence_count < 5:
        suggestions.append("Add more structured points to lengthen your speech.")
    if label == "NEGATIVE":
        suggestions.append("Use more positive wording to create a better impression.")
    if not suggestions:
        suggestions.append("You're doing great! Keep practicing.")
    return suggestions

def run_presentation_coach():
    choice = get_user_input()

    if choice == "1":
        text = get_text_from_voice()
    elif choice == "2":
        text = get_text_from_input()
    else:
        print("❌ Invalid choice. Please restart and enter 1 or 2.")
        return

    if "not recognized" in text or "API error" in text:
        print("⚠️ Error:", text)
        return

    label, confidence = analyze_sentiment(text)
    structure, sentence_count = structure_score(text)
    improvements = suggest_improvements(label, confidence, sentence_count)

    print("\n📊 Presentation Analysis")
    print(f"🧠 Sentiment: {label}")
    print(f"💪 Confidence Score: {confidence}/100")
    print(f"📐 Structure Score: {structure}/100")
    print("💡 Suggestions to Improve:")
    for tip in improvements:
        print(f" - {tip}")

if __name__ == "__main__":
    run_presentation_coach()
