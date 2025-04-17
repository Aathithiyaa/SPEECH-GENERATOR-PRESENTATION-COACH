import pyttsx3
from transformers import pipeline

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set up speech rate and volume (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to generate speech from text and play it
def generate_speech(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Hugging Face pipeline for text generation
generator = pipeline("text-generation", model="gpt2")

# Function to generate a structured speech based on the user's prompt
def generate_text(prompt):
    generated_text = generator(prompt, max_length=250, num_return_sequences=1)
    return generated_text[0]['generated_text']

# Main function
def main():
    # Get the speech prompt from the user
    user_prompt = input("Enter your speech prompt: ")

    # Generate the speech text
    print("\nGenerated Speech:\n")
    generated_speech = generate_text(user_prompt)
    print(generated_speech)

    # Convert the generated text to audio
    print("\nPlaying the generated speech...")
    generate_speech(generated_speech)

if __name__ == "__main__":
    main()

