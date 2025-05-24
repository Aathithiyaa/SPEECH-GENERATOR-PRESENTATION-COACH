import streamlit as st
import os
import sys

# Add error handling for imports
try:
    from speech_master import SpeechGenerator, PresentationCoach
    MODULES_LOADED = True
except ImportError as e:
    st.error(f"Error importing speech_master module: {str(e)}")
    st.error("Please make sure the speech_master.py file is in the same directory as app.py")
    MODULES_LOADED = False

# Page configuration
st.set_page_config(
    page_title="Speech Master AI",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Fixed and cleaned up
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
        border: 1px solid #e9ecef;
    }
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        margin-top: 3rem;
    }
    .feature-box {
        color: #555;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    .badge {
        background-color: #E3F2FD;
        color: #1976D2;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 5px;
        display: inline-block;
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
        border: 1px solid #ddd;
    }
    .stAlert > div {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'api_key_saved' not in st.session_state:
        st.session_state.api_key_saved = False
    
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    
    if 'coach' not in st.session_state and MODULES_LOADED:
        try:
            st.session_state.coach = PresentationCoach()
        except Exception as e:
            st.error(f"Error initializing PresentationCoach: {str(e)}")
            st.session_state.coach = None
    
    if 'last_speech' not in st.session_state:
        st.session_state.last_speech = None
        
    if 'last_audio' not in st.session_state:
        st.session_state.last_audio = None

# Initialize session state
initialize_session_state()

# Main header
st.markdown('<h1 class="main-header">🎤 Speech Master AI</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo handling with error checking
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=300)
    else:
        st.markdown("### 🎤 Speech Master AI")
        st.info("Logo not found. Please add logo.png to assets/ folder.")

    st.markdown("### Navigation")
    page = st.radio("Choose a tool:", ["📝 Speech Generator", "🎯 Presentation Coach", "ℹ️ About"])
    
    st.markdown("### Configuration")
    
    # API Key configuration
    with st.expander("API Key Settings", expanded=not st.session_state.api_key_saved):
        api_key = st.text_input("Groq API Key:", type="password", 
                              help="Enter your Groq API Key to enable speech generation")
        if st.button("Save API Key"):
            if api_key and MODULES_LOADED:
                try:
                    st.session_state.generator = SpeechGenerator(api_key)
                    st.session_state.api_key_saved = True
                    st.success("API key saved successfully!")
                    st.rerun()  # Refresh the app
                except Exception as e:
                    st.error(f"Error setting API key: {str(e)}")
            elif not MODULES_LOADED:
                st.error("Cannot save API key: speech_master module not loaded")
            else:
                st.warning("Please enter an API key")

    st.markdown("---")
    st.markdown('<p class="footer">Created with ❤️ by Aadhi Speech Master AI<br>© 2025</p>', unsafe_allow_html=True)

# Check if modules are loaded before proceeding
if not MODULES_LOADED:
    st.error("⚠️ Core modules are not loaded. Please check your speech_master.py file.")
    st.stop()

# Page content
if page == "📝 Speech Generator":
    st.markdown('<h2 class="sub-header">AI Speech Generator</h2>', unsafe_allow_html=True)
    
    if not st.session_state.api_key_saved:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to use the Speech Generator.")
        
        # Show sample content when API key is not set
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("**🎯 What you can do with Speech Generator:**")
        st.markdown("• Create professional speeches tailored to your needs")
        st.markdown("• Customize style, duration, audience, and more")
        st.markdown("• Get ready-to-deliver content with speaking notes")
        st.markdown("• Convert text to speech audio")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.write("Create professional speeches tailored to your needs. Customize style, duration, audience, and more. Get ready-to-deliver content with speaking notes included!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Speech Configuration", expanded=True):
                topic = st.text_input("Speech Topic:", value="Artificial Intelligence in Education")
                duration = st.slider("Duration (minutes):", 1, 15, 3)
                
                # Safe access to style templates
                try:
                    emotion_options = list(SpeechGenerator.STYLE_TEMPLATES.keys())
                    emotion = st.selectbox("Speech Style:", options=emotion_options)
                except AttributeError:
                    emotion = st.selectbox("Speech Style:", options=["professional", "casual", "motivational"])
                
                try:
                    audience_options = list(SpeechGenerator.AUDIENCE_GUIDANCE.keys())
                    audience = st.selectbox("Target Audience:", options=audience_options)
                except AttributeError:
                    audience = st.selectbox("Target Audience:", options=["general", "academic", "business"])
        
        with col2:
            with st.expander("Advanced Settings", expanded=True):
                # Safe access to available models
                try:
                    model_options = list(SpeechGenerator.AVAILABLE_MODELS.keys())
                    model = st.selectbox(
                        "LLM Model:", 
                        options=model_options,
                        format_func=lambda x: f"{x} - {SpeechGenerator.AVAILABLE_MODELS[x]['description']}"
                    )
                except AttributeError:
                    model = st.selectbox("LLM Model:", options=["llama3-8b-8192"])
                
                temperature = st.slider("Creativity (Temperature):", 0.1, 1.0, 0.7, 0.1)
                voice_type = st.radio("Text-to-Speech Voice:", options=["male", "female"])
                additional_instructions = st.text_area("Additional Instructions:", 
                                                   placeholder="E.g., Include a personal anecdote", 
                                                   max_chars=200)
        
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
                    
                    st.success(f"✅ Speech generated successfully with {metadata['word_count']} words (~{duration} minutes)")
                    
                except Exception as e:
                    st.error(f"Error generating speech: {str(e)}")
        
        # Display generated speech
        if st.session_state.last_speech:
            st.markdown("### Generated Speech")
            
            if 'last_metadata' in st.session_state:
                meta = st.session_state.last_metadata
                col_badge1, col_badge2, col_badge3, col_badge4 = st.columns(4)
                with col_badge1:
                    st.markdown(f'<span class="badge">Topic: {meta["topic"]}</span>', unsafe_allow_html=True)
                with col_badge2:
                    st.markdown(f'<span class="badge">Style: {meta["emotion"]}</span>', unsafe_allow_html=True)
                with col_badge3:
                    st.markdown(f'<span class="badge">Audience: {meta["audience"]}</span>', unsafe_allow_html=True)
                with col_badge4:
                    st.markdown(f'<span class="badge">Words: {meta["word_count"]}</span>', unsafe_allow_html=True)
            
            speech_text = st.session_state.last_speech
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(speech_text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Audio generation controls
            audio_col1, audio_col2 = st.columns([3, 1])
            
            with audio_col1:
                if st.button("🔊 Generate Audio from Speech", use_container_width=True):
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
                if st.session_state.last_audio and os.path.exists(st.session_state.last_audio):
                    try:
                        with open(st.session_state.last_audio, "rb") as audio_file:
                            st.download_button(
                                label="📥 Download Audio",
                                data=audio_file.read(),
                                file_name="speech_audio.mp3",
                                mime="audio/mp3",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"Error loading audio file: {str(e)}")
            
            # Audio player
            if st.session_state.last_audio and os.path.exists(st.session_state.last_audio):
                st.audio(st.session_state.last_audio)
            
            # Download speech text
            st.download_button(
                label="📄 Download Speech Text",
                data=speech_text,
                file_name=f"speech_{topic.replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )

elif page == "🎯 Presentation Coach":
    st.markdown('<h2 class="sub-header">Presentation Coach</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("**🎯 Analyze Your Speech Delivery**")
    st.write("Get instant feedback on sentiment, structure, complexity, and delivery improvements. Perfect for rehearsing your presentations!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_speech = st.text_area(
        "Enter your speech or presentation here:",
        height=200,
        placeholder="Paste your speech or draft presentation text here for analysis...",
        help="Enter at least 50 words for meaningful analysis"
    )
    
    if st.button("🔍 Analyze Speech", type="primary", use_container_width=True):
        if not user_speech.strip():
            st.warning("Please enter some text to analyze.")
        elif len(user_speech.split()) < 10:
            st.warning("Please enter at least 10 words for meaningful analysis.")
        else:
            with st.spinner("Analyzing your speech..."):
                try:
                    coach = st.session_state.coach
                    
                    if coach is None:
                        st.error("Presentation Coach is not available. Please restart the application.")
                    else:
                        # Perform analysis
                        sentiment_label, confidence = coach.analyze_sentiment(user_speech)
                        structure_score, sentence_count = coach.structure_score(user_speech)
                        complexity_score = coach.analyze_complexity(user_speech)
                        suggestions = coach.suggest_improvements(sentiment_label, confidence, sentence_count, complexity_score)
                        
                        st.markdown('<div class="results-container">', unsafe_allow_html=True)
                        
                        # Analysis results
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("### 😊 Sentiment")
                            sentiment_color = "#28a745" if sentiment_label == "POSITIVE" else "#dc3545" if sentiment_label == "NEGATIVE" else "#007bff"
                            st.markdown(f"<h2 style='color: {sentiment_color}; text-align: center;'>{sentiment_label}</h2>", unsafe_allow_html=True)
                            st.progress(confidence/100)
                            st.caption(f"Confidence: {confidence:.1f}%")
                        
                        with col2:
                            st.markdown("### 📋 Structure")
                            st.markdown(f"<h2 style='text-align: center; color: #1E88E5;'>{structure_score}/100</h2>", unsafe_allow_html=True)
                            st.progress(structure_score/100)
                            st.caption(f"Based on {sentence_count} sentences")
                        
                        with col3:
                            st.markdown("### 🧠 Complexity")
                            st.markdown(f"<h2 style='text-align: center; color: #1E88E5;'>{complexity_score}/100</h2>", unsafe_allow_html=True)
                            st.progress(complexity_score/100)
                            complexity_level = "High" if complexity_score > 70 else "Medium" if complexity_score > 40 else "Low"
                            st.caption(f"Language complexity: {complexity_level}")
                        
                        # Improvement suggestions
                        st.markdown("### 💡 Improvement Suggestions")
                        if suggestions:
                            for i, suggestion in enumerate(suggestions, 1):
                                st.markdown(f"{i}. {suggestion}")
                        else:
                            st.info("Your speech looks great! No specific suggestions at this time.")
                        
                        # Speech statistics
                        words = user_speech.split()
                        word_count = len(words)
                        estimated_time = round(word_count / 130, 1)  # Average speaking pace
                        char_count = len(user_speech)
                        
                        st.markdown("### 📊 Speech Statistics")
                        stats_col1, stats_col2, stats_col3 = st.columns(3)
                        with stats_col1:
                            st.metric("Word Count", f"{word_count:,}")
                        with stats_col2:
                            st.metric("Estimated Time", f"{estimated_time} min")
                        with stats_col3:
                            st.metric("Character Count", f"{char_count:,}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error analyzing speech: {str(e)}")
                    st.error("Please make sure all required components are properly installed.")

elif page == "ℹ️ About":
    st.markdown('<h2 class="sub-header">About Speech Master AI</h2>', unsafe_allow_html=True)
    
    # Project Overview Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Project Overview")
    st.write("Speech Master AI is a comprehensive toolkit for speech preparation and delivery, combining AI-powered speech generation with intelligent presentation coaching.")
    
    st.markdown("### ✨ Features")
    st.markdown('<p><span class="highlight">Speech Generator:</span> Create professional speeches tailored for any occasion with customizable styles, audience targeting, and text-to-speech capabilities.</p>', unsafe_allow_html=True)
    st.markdown('<p><span class="highlight">Presentation Coach:</span> Analyze your speeches to receive feedback on sentiment, structure, complexity, and delivery improvements.</p>', unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Technology Stack")
    st.markdown("- **Streamlit** - Interactive web interface")
    st.markdown("- **Groq API** - Large language model integration") 
    st.markdown("- **pyttsx3** - Text-to-speech synthesis")
    st.markdown("- **NLTK** - Natural language processing")
    
    st.markdown("### 🚀 Getting Started")
    st.write("To use the Speech Generator, you'll need to provide a Groq API key in the sidebar settings. The Presentation Coach works offline without requiring any API keys.")
    
    st.markdown("### 🔧 Troubleshooting")
    st.write("If you encounter issues:")
    st.markdown("- Make sure all required modules are installed")
    st.markdown("- Check that your Groq API key is valid") 
    st.markdown("- Ensure the speech_master.py file is in the same directory")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📈 Project Statistics")
    
    # Statistics with error handling
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        model_count = len(SpeechGenerator.AVAILABLE_MODELS) if hasattr(SpeechGenerator, 'AVAILABLE_MODELS') else 4
        style_count = len(SpeechGenerator.STYLE_TEMPLATES) if hasattr(SpeechGenerator, 'STYLE_TEMPLATES') else 8
        audience_count = len(SpeechGenerator.AUDIENCE_GUIDANCE) if hasattr(SpeechGenerator, 'AUDIENCE_GUIDANCE') else 6
    except:
        model_count, style_count, audience_count = 4, 8, 6
    
    col1.metric("Supported Models", model_count)
    col2.metric("Speech Styles", style_count)
    col3.metric("Audience Types", audience_count)
    col4.metric("Voice Options", 2)
    
    # System information
    with st.expander("System Information"):
        st.write(f"Python version: {sys.version}")
        st.write(f"Streamlit version: {st.__version__}")
        st.write(f"Working directory: {os.getcwd()}")
        st.write(f"Modules loaded: {'✅' if MODULES_LOADED else '❌'}")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-size: 0.8rem;">Built with Streamlit • Powered by Groq API</p>', 
    unsafe_allow_html=True
)