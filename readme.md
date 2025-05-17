# Speech Master AI

A comprehensive AI-powered toolkit for speech preparation and delivery, featuring speech generation and presentation coaching capabilities.

## Features

### Speech Generator

- Create professional speeches tailored for any occasion
- Customize speech style, duration, and target audience
- Select from multiple LLM models for different quality levels
- Convert text to speech with male and female voice options
- Download speech content as text or audio files

### Presentation Coach

- Analyze speech sentiment, structure, and complexity
- Receive instant feedback on your presentation delivery
- Get personalized improvement suggestions
- Track key speech statistics like word count and estimated delivery time

## Technology Stack

- **Frontend**: Streamlit for interactive web interface
- **AI Models**: Groq API for LLM access (Llama, Gemma, Mixtral)
- **Text-to-Speech**: pyttsx3 for speech synthesis
- **Natural Language Processing**: NLTK for speech analysis

## Requirements

- Python 3.8+
- Groq API key (for speech generation)
- See `requirements.txt` for Python package dependencies

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/speech-master-ai.git
   cd speech-master-ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

## API Key Setup

To use the Speech Generator feature, you'll need a Groq API key:

1. Sign up at [Groq](https://console.groq.com/signup) to get your API key
2. Enter your API key in the sidebar settings section of the app
3. The Presentation Coach works offline and doesn't require an API key

## Models & Styles

### Available LLM Models

| Model | Description | Max Tokens |
|-------|-------------|------------|
| llama3-8b-8192 | Balanced model for general use | 8,192 |
| llama3-70b-8192 | Advanced model with better quality | 8,192 |
| gemma-7b-it | Efficient model for simpler tasks | 4,096 |
| mixtral-8x7b-32768 | High-capacity model for longer context | 32,768 |

### Speech Styles

- Formal
- Casual
- Motivational
- Persuasive
- Instructional
- Debate
- Humorous
- Storytelling

### Audience Types

- General
- Experts
- Children
- Students
- Executives
- International

## Project Structure

- `app.py` - Main Streamlit application
- `speech_master.py` - Core functionality module
- `speech_outputs/` - Directory for generated speech files

## License

[MIT License](LICENSE)

## Author

Created by @AadhithyaPrakash, @Aathithiyaa @Aasis-Mohamed2208, @Jeeva2309 © 2025
