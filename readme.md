# AI Speech Generator and Presentation Coach

This project provides a modular and extensible framework for generating, analyzing, and vocalizing public speeches using large language models (LLMs) and speech processing libraries.

## Features

### 1. Presentation Coach

- Supports speech input via microphone or manual text
- Performs sentiment analysis using HuggingFace Transformers
- Evaluates structural clarity based on sentence count
- Generates improvement suggestions based on delivery quality

### 2. Speech Generator with Audio Support

- Customizable tone styles: formal, motivational, persuasive, debate, humorous, instructional, and storytelling
- Tailors speeches for target audiences such as students, experts, executives, or children
- Provides text-to-speech (TTS) synthesis using `pyttsx3` with configurable voice settings
- Jupyter-based interactive user interface using `ipywidgets`

## Installation

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

Or manually install the core libraries:

```bash
pip install transformers torch torchaudio speechrecognition pyttsx3 ipywidgets groq
```

## File Structure

```speech-generator-presentation-coach/
├── .venv/                     # Python virtual environment
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── groq_api_key.json          # Groq API key (excluded from version control)
├── GEN_SPEECH.ipynb           # Jupyter notebook interface
├── pres.py                    # Script for presentation coach or CLI logic
```

## Usage

### CLI Mode: Presentation Coach

To run the command-line based speech analyzer:

```bash
python code.txt
```

### Jupyter Notebook Mode: Speech Generator Interface

To use the interactive GUI, run the last cell in a Jupyter Notebook.

## API Key Configuration (Groq)

Create a `groq_api_key.json` file in your project directory or user home directory:

```json
{
  "groq_api_key": "your-groq-api-key"
}
```

The application will attempt to load the key from:

- `~/groq_api_key.json`
- `./groq_api_key.json`

## Available LLM Models

The following Groq-supported models are pre-integrated:

| Model                | Description                            | Max Tokens |
|---------------------|----------------------------------------|------------|
| llama3-8b-8192       | Balanced general-purpose model         | 8192       |
| llama3-70b-8192      | High-performance advanced model        | 8192       |
| gemma-7b-it          | Efficient for lightweight generation   | 4096       |
| mixtral-8x7b-32768   | Long-context model for extended speech | 32768      |

## Voice Configuration

Text-to-speech voice settings are available for:

- Male
- Female

## Future Enhancements

- Web-based interface using Flask or FastAPI
- Speech export as PDF
- Emotion-aligned TTS delivery
- User authentication and cloud-based history

## License

This project is released under the MIT License.

## Acknowledgments

- HuggingFace Transformers
- Groq API for LLM inference
- NLTK for text tokenization
- pyttsx3 for TTS synthesis
