import streamlit as st
import os
import base64
from typing import Dict
import tempfile
import sys
import time

# Import the core functionality
# Assuming the core file is named "speech_master_core.py"
from speech_master import SpeechGenerator, PresentationCoach, get_binary_file_downloader_html

# Page configuration
st.set_page_config(
    page_title="Speech Master AI",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 500;
        color: #333;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        margin-top: 3rem;
    }
    .feature-box {
        font-color: #555;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        margin-bottom: 10px;
    }
    .badge {
        background-color: #E3F2FD;
        color: #1976D2;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .highlight {
        color: #1E88E5;
        font-weight: 600;
    }
    .results-container {
        padding: 15px;
        background-color: #f5f5f5;
        border-radius: 8px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# App state initialization
if 'api_key_saved' not in st.session_state:
    st.session_state.api_key_saved = False

if 'generator' not in st.session_state:
    st.session_state.generator = None

if 'coach' not in st.session_state:
    st.session_state.coach = PresentationCoach()

if 'last_speech' not in st.session_state:
    st.session_state.last_speech = None
    
if 'last_audio' not in st.session_state:
    st.session_state.last_audio = None

# App Navigation
st.markdown('<h1 class="main-header">🎤 Speech Master AI</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Speech+AI", width=150)
    st.markdown("### Navigation")
    page = st.radio("Choose a tool:", ["📝 Speech Generator", "🎯 Presentation Coach", "ℹ️ About"])
    
    # API Key Input (in sidebar)
    st.markdown("### Configuration")
    with st.expander("API Key Settings", expanded=not st.session_state.api_key_saved):
        api_key = st.text_input("Groq API Key:", type="password", 
                              help="Enter your Groq API Key to enable speech generation")
        if st.button("Save API Key"):
            if api_key:
                try:
                    st.session_state.generator = SpeechGenerator(api_key)
                    st.session_state.api_key_saved = True
                    st.success("API key saved successfully!")
                except Exception as e:
                    st.error(f"Error setting API key: {str(e)}")
            else:
                st.warning("Please enter an API key")

    # Footer in sidebar
    st.markdown("---")
    st.markdown('<p class="footer">Created with ❤️ by Aadhi Speech Master AI © 2025</p>', unsafe_allow_html=True)


# Main content area
if page == "📝 Speech Generator":
    st.markdown('<h2 class="sub-header">AI Speech Generator</h2>', unsafe_allow_html=True)
    
    if not st.session_state.api_key_saved:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to use the Speech Generator.")
    else:
        st.markdown("""
        <div class="feature-box">
            Create professional speeches tailored to your needs. Customize style, duration, 
            audience, and more. Get ready-to-deliver content with speaking notes included!
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Speech Configuration"):
                topic = st.text_input("Speech Topic:", value="Artificial Intelligence in Education")
                duration = st.slider("Duration (minutes):", 1, 15, 3)
                emotion = st.selectbox("Speech Style:", options=list(SpeechGenerator.STYLE_TEMPLATES.keys()))
                audience = st.selectbox("Target Audience:", options=list(SpeechGenerator.AUDIENCE_GUIDANCE.keys()))
        
        with col2:
            with st.expander("Advanced Settings"):
                model = st.selectbox(
                    "LLM Model:", 
                    options=list(SpeechGenerator.AVAILABLE_MODELS.keys()),
                    format_func=lambda x: f"{x} - {SpeechGenerator.AVAILABLE_MODELS[x]['description']}"
                )
                temperature = st.slider("Creativity (Temperature):", 0.1, 1.0, 0.7, 0.1)
                voice_type = st.radio("Text-to-Speech Voice:", options=["male", "female"])
                additional_instructions = st.text_area("Additional Instructions:", 
                                                   placeholder="E.g., Include a personal anecdote", max_chars=200)
        
        # Generate speech button
        if st.button("Generate Speech", type="primary", use_container_width=True):
            with st.spinner("Generating your speech... This may take a moment"):
                try:
                    speech_text, metadata = st.session_state.generator.generate_speech(
                        topic=topic,
                        duration=duration,
                        emotion=emotion,
                        audience=audience,
                        model=model,
                        temperature=temperature,
                        additional_instructions=additional_instructions
                    )
                    st.session_state.last_speech = speech_text
                    st.session_state.last_metadata = metadata
                    
                    # Display success message
                    st.success(f"✅ Speech generated successfully with {metadata['word_count']} words (~{duration} minutes)")
                    
                except Exception as e:
                    st.error(f"Error generating speech: {str(e)}")
        
        # Display generated speech if available
        if st.session_state.last_speech:
            st.markdown("### Generated Speech")
            
            # Speech metadata
            if 'last_metadata' in st.session_state:
                meta = st.session_state.last_metadata
                st.markdown(f"""
                <p>
                <span class="badge">Topic: {meta['topic']}</span> 
                <span class="badge">Style: {meta['emotion']}</span> 
                <span class="badge">Audience: {meta['audience']}</span> 
                <span class="badge">Words: {meta['word_count']}</span>
                </p>
                """, unsafe_allow_html=True)
            
            speech_text = st.session_state.last_speech
            
            # Display speech content
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(speech_text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Audio generation
            audio_col1, audio_col2 = st.columns([3, 1])
            
            with audio_col1:
                if st.button("Generate Audio from Speech", use_container_width=True):
                    with st.spinner("Converting text to speech..."):
                        try:
                            audio_path = st.session_state.generator.generate_speech_audio(
                                text=speech_text,
                                voice=voice_type
                            )
                            st.session_state.last_audio = audio_path
                            st.success("Audio generated successfully!")
                        except Exception as e:
                            st.error(f"Error generating audio: {str(e)}")
            
            with audio_col2:
                if st.session_state.last_audio:
                    st.download_button(
                        label="Download Audio",
                        data=open(st.session_state.last_audio, "rb").read(),
                        file_name="speech_audio.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            
            # Audio player
            if st.session_state.last_audio:
                st.audio(st.session_state.last_audio)
                
            # Download text option
            st.download_button(
                label="Download Speech Text",
                data=speech_text,
                file_name=f"speech_{SpeechGenerator._sanitize_filename(topic)}.txt",
                mime="text/plain",
                use_container_width=True
            )

elif page == "🎯 Presentation Coach":
    st.markdown('<h2 class="sub-header">Presentation Coach</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-box">
        Analyze your speech delivery and get instant feedback on sentiment, 
        structure, and more. Perfect for rehearsing your presentations!
    </div>
    """, unsafe_allow_html=True)
    
    # Text input for speech
    user_speech = st.text_area(
        "Enter your speech or presentation here:",
        height=200,
        placeholder="Paste your speech or draft presentation text here for analysis..."
    )
    
    # Analyze button
    if st.button("Analyze Speech", type="primary", use_container_width=True) and user_speech:
        with st.spinner("Analyzing your speech..."):
            # Get the coach from session state
            coach = st.session_state.coach
            
            # Perform analysis
            sentiment_label, confidence = coach.analyze_sentiment(user_speech)
            structure_score, sentence_count = coach.structure_score(user_speech)
            complexity_score = coach.analyze_complexity(user_speech)
            suggestions = coach.suggest_improvements(sentiment_label, confidence, sentence_count, complexity_score)
            
            # Display results
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            # Results in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"### Sentiment")
                sentiment_color = "green" if sentiment_label == "POSITIVE" else "red" if sentiment_label == "NEGATIVE" else "blue"
                st.markdown(f"<h2 style='color: {sentiment_color}; text-align: center;'>{sentiment_label}</h2>", unsafe_allow_html=True)
                st.progress(confidence/100)
                st.caption(f"Confidence: {confidence:.1f}%")
            
            with col2:
                st.markdown(f"### Structure")
                st.markdown(f"<h2 style='text-align: center;'>{structure_score}/100</h2>", unsafe_allow_html=True)
                st.progress(structure_score/100)
                st.caption(f"Based on {sentence_count} sentences")
            
            with col3:
                st.markdown(f"### Complexity")
                st.markdown(f"<h2 style='text-align: center;'>{complexity_score}/100</h2>", unsafe_allow_html=True)
                st.progress(complexity_score/100)
                complexity_level = "High" if complexity_score > 70 else "Medium" if complexity_score > 40 else "Low"
                st.caption(f"Language complexity: {complexity_level}")
            
            # Suggestions
            st.markdown("### Improvement Suggestions")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
            
            # Word count stats
            words = user_speech.split()
            word_count = len(words)
            estimated_time = round(word_count / 130, 1)  # Assuming 130 words per minute
            
            st.markdown("### Speech Statistics")
            st.markdown(f"- Word count: **{word_count}** words")
            st.markdown(f"- Estimated delivery time: **{estimated_time}** minutes")
            
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "ℹ️ About":
    st.markdown('<h2 class="sub-header">About Speech Master AI</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h3>Project Overview</h3>
        <p>Speech Master AI is a comprehensive toolkit for speech preparation and delivery, 
        combining AI-powered speech generation with presentation coaching.</p>
        
        <h3>Features</h3>
        <p><span class="highlight">Speech Generator:</span> Create professional speeches tailored for any occasion
        with customizable styles, audience targeting, and text-to-speech capabilities.</p>
        
        <p><span class="highlight">Presentation Coach:</span> Analyze your speeches to receive feedback on sentiment,
        structure, and delivery improvements.</p>
        
        <h3>Technology Stack</h3>
        <ul>
            <li>Streamlit for the interactive web interface</li>
            <li>Groq API for large language model integration</li>
            <li>pyttsx3 for text-to-speech synthesis</li>
            <li>NLTK for natural language processing</li>
        </ul>
        
        <h3>Getting Started</h3>
        <p>To use the Speech Generator, you'll need to provide a Groq API key in the sidebar settings.
        The Presentation Coach works offline without requiring any API keys.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project statistics
    st.markdown("### Project Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supported Models", "4")
    col2.metric("Speech Styles", "8")
    col3.metric("Audience Types", "6")
    col4.metric("Voice Options", "2")

# Run the app
if __name__ == "__main__":
    # Check if core module is available
    try:
        # Just a simple version check - you can expand this
        if not hasattr(SpeechGenerator, 'STYLE_TEMPLATES'):
            st.error("Error: Core functionality module not loaded correctly.")
    except Exception as e:
        st.error(f"Error loading core module: {str(e)}")