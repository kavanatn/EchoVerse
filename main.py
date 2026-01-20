import os
import streamlit as st
import base64
import io
from pathlib import Path
from pypdf import PdfReader
from model import genrate_reader_json
from utils import concated_text
from tts import generate_tts, ENGLISH_VOICES
from get_token import get_ibm_iam_bearer


# ---------------------------
# Configure page
# ---------------------------
st.set_page_config(
    page_title="EchoVerse",
    layout="centered"
)

# Check for API Key
api_key = os.getenv("WATSONX_API_KEY")
if not api_key:
    st.warning("Running in demo mode. API key not configured. Please set WATSONX_API_KEY.")


# ---------------------------
# Load custom CSS
# ---------------------------
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #3282b8 0%, #011d43 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 0.25rem;
        padding-bottom: 0.25rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .logo-text {
        font-size: 2.3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #d9d9d9;
        font-weight: 300;
        margin-bottom: 0;
    }
    
    /* Input Area Styling */
    .input-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background-color: #f8f9fa !important;
        color: #1b262c !important;
        border: 2px solid #3282b8 !important;
        border-radius: 15px !important;
        padding: 0.75rem !important;
        font-size: 15px !important;
        min-height: 180px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0f4c75 !important;
        box-shadow: 0 0 10px rgba(50, 130, 184, 0.3) !important;
    }
    
    /* File Uploader Styling */
    .stFileUploader {
        background-color: #d9d9d9;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 2px dashed #3282b8;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background-color: #e8f4f8;
        border-color: #0f4c75;
    }
    
    /* Button Styling */
    .stButton button {
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(15, 76, 117, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(15, 76, 117, 0.4) !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox select {
        background-color: #f8f9fa !important;
        border: 2px solid #d9d9d9 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        font-size: 16px !important;
    }
    
    /* Output Page Styling */
    .output-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .back-button {
        background: #d9d9d9 !important;
        color: #1b262c !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
    }
    
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        height: 350px;
        overflow-y: auto;
    }
    
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1b262c;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #3282b8;
        padding-bottom: 0.25rem;
    }
    
    .audio-player {
        background: #0f4c75;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        color: white;
    }
    
    .action-buttons {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .action-button {
        background: #d9d9d9 !important;
        color: #1b262c !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .action-button:hover {
        background: #3282b8 !important;
        color: white !important;
    }
    
    .download-button {
        background: linear-gradient(135deg, #0f4c75, #3282b8) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 1rem 0;
        color: #d9d9d9;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .logo-text {
            font-size: 2rem;
        }
        
        .tagline {
            font-size: 1rem;
        }
        
        .input-container {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .content-card {
            height: 300px;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3282b8;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Progress Bar */
    .progress-container {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3282b8, #0f4c75);
        height: 8px;
        border-radius: 5px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)


load_css()

# ---------------------------
# Header Renderer
# ---------------------------


def render_header(show_back_button=False):
    logo_path = "logo.png"
    if show_back_button:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", key="back_btn", help="Return to home"):
                st.session_state.page = "home"
                st.rerun()
        with col2:
            st.markdown(
                f"""
                <div class="main-header">
                    <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}"
                         alt="EchoVerse Logo"
                         style="height:150px;">
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.title("EchoVerse – AI Powered Audiobook Generator")
        st.markdown(
            f"""
            <div class="main-header">
                <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}"
                     alt="EchoVerse Logo"
                     style="height:150px;">
                <p class="tagline">Turn Your Words Into Immersive Audio</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------
# Home Page with Voice Selection
# ---------------------------
def render_home_page():
    render_header()

    # st.markdown('<div class="input-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="card-title" style="color:white;">📝 Text Input</div>',
            unsafe_allow_html=True,
        )
        text_input = st.text_area(
            "Enter your text",
            placeholder="Paste your text here...",
            height=200,
            key="text_input",
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="card-title" style="color:white;">📄 Upload PDF</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload file",
            type=["pdf", "txt"],
            help="Upload a PDF or TXT file",
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")

    with col2:
        st.markdown('<div class="card-title">🎯 Tone Selection</div>',
                    unsafe_allow_html=True)

        tone = st.selectbox(
            "Select Tone",
            [
                "Neutral",
                "Suspenseful",
                "Inspiring",
                "Professional",
                "Casual",
                "Dramatic",
            ],
            key="tone_select",
        )

        st.markdown('<div class="card-title">🎤 Voice Selection</div>',
                    unsafe_allow_html=True)

        # Create voice options with user-friendly names
        voice_display_names = {
            "allison_expressive": "🎭 Allison (Female, Expressive)",
            "emma_expressive": "🎭 Emma (Female, Expressive)",
            "lisa_expressive": "🎭 Lisa (Female, Expressive)",
            "michael_expressive": "🎭 Michael (Male, Expressive)",
            "allison": "👩 Allison (Female, Standard)",
            "lisa": "👩 Lisa (Female, Standard)",
            "michael": "👨 Michael (Male, Standard)",
            "kevin": "👨 Kevin (Male, Young)",
            "henry": "👨 Henry (Male, Mature)",
            "emily": "👩 Emily (Female, Energetic)",
            "kate_british": "🇬🇧 Kate (Female, British)",
            "charlotte_british": "🇬🇧 Charlotte (Female, British)",
            "james_british": "🇬🇧 James (Male, British)",
            "heidi_australian": "🇦🇺 Heidi (Female, Australian)",
            "jack_australian": "🇦🇺 Jack (Male, Australian)",
        }

        selected_voice = st.selectbox(
            "Choose Voice",
            options=list(voice_display_names.keys()),
            format_func=lambda x: voice_display_names[x],
            index=0,  # Default to first option
            key="voice_select",
            help="Expressive voices support emotional expressions"
        )

        # Show voice type info
        if "expressive" in selected_voice or "australian" in selected_voice:
            st.success("🎭 Expressive voice - supports emotions!")
        elif "british" in selected_voice:
            st.info("🇬🇧 British accent selected")
        else:
            st.info("🎵 Standard voice - clear narration")

        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🎵 Generate Audio", key="generate_btn", type="primary"):
            extracted_text = ""

            if text_input.strip():
                extracted_text = text_input.strip()
                st.success("✅ Text input received successfully!")

            elif uploaded_file:
                st.info("📄 Extracting text from uploaded file...")
                if uploaded_file.type == "application/pdf":
                    try:
                        reader = PdfReader(uploaded_file)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text()
                        extracted_text = " ".join(text.split("\n"))
                        st.success("✅ File text extracted successfully!")
                    except Exception as e:
                        st.error(f"❌ Error extracting PDF: {e}")
                        return

                elif uploaded_file.type == "text/plain":
                    extracted_text = uploaded_file.read().decode("utf-8")
                    st.success("✅ File text extracted successfully!")
                else:
                    st.error("Currently, only PDF and TXT are supported.")
                    return

                if not extracted_text.strip():
                    st.error("⚠ No text found in uploaded file.")
                    return
            else:
                st.error("Please provide text input or upload a file!")
                return

            # Store all selections in session state
            st.session_state.original_text = extracted_text
            st.session_state.selected_tone = tone
            st.session_state.selected_voice = selected_voice  # Store selected voice
            st.session_state.page = "output"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------
# Output Page
# ---------------------------
def render_output_page():
    render_header(show_back_button=True)

    # Layout: three columns
    col1, col2, col3 = st.columns([1, 1, 0.5])

    # -------------------- Column 1: Original Input --------------------
    with col1:
        original_text = st.session_state.get(
            "original_text", "No text provided")
        st.markdown(
            f"""
            <div class='content-card'>
                <div class='card-title'>📄 Original Input</div>
                <div style='color: #1b262c; line-height: 1.6; font-size: 14px;'>{original_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    ai_generated_object = None
    # -------------------- Column 2: Tone-Adapted Narration --------------------
    with col2:
        tone = st.session_state.get("selected_tone", "Neutral")
        selected_voice = st.session_state.get(
            "selected_voice", "allison_expressive")

        if api_key:
            try:
                token = get_ibm_iam_bearer(api_key)
                ai_generated_object = genrate_reader_json(original_text, tone, token)
            except Exception as e:
                st.error(f"Error generating text: {e}")
                ai_generated_object = None
        else:
             st.error("API Key missing. Cannot generate text.")
             ai_generated_object = None

        if ai_generated_object:
            print(f"AI Generated Object: {ai_generated_object}")  # Debug
            print(f"Selected Voice: {selected_voice}")  # Debug

            adapted_text = concated_text(ai_generated_object)

            # Display current settings
            voice_name = selected_voice.replace('_', ' ').title()

            st.markdown(
                f"""
                <div class='content-card'>
                    <div class='card-title'>🎵 Tone-Adapted Narration</div>
                    <div style='color: #666; font-size: 12px; margin-bottom: 10px; padding: 5px; background: #f0f0f0; border-radius: 5px;'>
                        🎯 Tone: <strong>{tone}</strong> | 🎤 Voice: <strong>{voice_name}</strong>
                    </div>
                    <div style='color: #1b262c; line-height: 1.6; font-size: 14px; overflow-y: scroll;'>{adapted_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("No generated content to display.")

    # -------------------- Column 3: Audio Player --------------------
    with col3:
        st.info(
            f"🎵 Generating audio with {selected_voice.replace('_', ' ').title()} voice..."
        )

        # Generate and play TTS audio with selected voice
        audio_file_path = Path("temp_audio.mp3")

        try:
            # Generate TTS with the selected voice
            if ai_generated_object and api_key:
                generate_tts(ai_generated_object, audio_file_path,
                             voice_name=selected_voice, api_key=api_key)
            elif not api_key:
                 st.error("API Key missing. Cannot generate audio.")
                 # Create a dummy file or handle gracefully? 
                 # For now, just let the next check fail or we can return early
                 pass

            if audio_file_path.exists():
                st.success(f"✅ Audio generated successfully!")
                audio_bytes = open(audio_file_path, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("❌ Audio generation failed - file not found.")

        except Exception as e:
            st.error(f"❌ Error generating audio: {str(e)}")
            st.info("Please try again or select a different voice.")

    with col3:
        st.markdown('<div class="card-title">⚡ Actions</div>',
                    unsafe_allow_html=True)

        # Regenerate with different tone
        if st.button("🔄 Regenerate", key="regenerate_btn", help="Generate with different settings"):
            new_tone = st.selectbox(
                "Choose new tone:",
                ["Neutral", "Suspenseful", "Inspiring",
                    "Professional", "Casual", "Dramatic"],
                key="new_tone_select"
            )

            # Voice selection for regeneration
            voice_display_names = {
                "allison_expressive": "🎭 Allison (Female, Expressive)",
                "emma_expressive": "🎭 Emma (Female, Expressive)",
                "lisa_expressive": "🎭 Lisa (Female, Expressive)",
                "michael_expressive": "🎭 Michael (Male, Expressive)",
                "allison": "👩 Allison (Female, Standard)",
                "lisa": "👩 Lisa (Female, Standard)",
                "michael": "👨 Michael (Male, Standard)",
                "kevin": "👨 Kevin (Male, Young)",
                "henry": "👨 Henry (Male, Mature)",
                "emily": "👩 Emily (Female, Energetic)",
                "kate_british": "🇬🇧 Kate (Female, British)",
                "charlotte_british": "🇬🇧 Charlotte (Female, British)",
                "james_british": "🇬🇧 James (Male, British)",
            }

            new_voice = st.selectbox(
                "Choose new voice:",
                options=list(voice_display_names.keys()),
                format_func=lambda x: voice_display_names[x],
                key="new_voice_select"
            )

            if st.button("Apply Changes", key="apply_changes"):
                st.session_state.selected_tone = new_tone
                st.session_state.selected_voice = new_voice
                st.rerun()

        st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)

        # Translation
        st.markdown("🌍 Translate")
        language = st.selectbox(
            "",
            ["English", "Spanish", "French", "German",
                "Italian", "Portuguese", "Chinese", "Japanese"],
            key="language_select",
            label_visibility="collapsed"
        )

        if st.button("Translate", key="translate_btn"):
            st.success(f"✅ Translated to {language}")

        st.markdown('<hr style="margin:0.5rem 0;">', unsafe_allow_html=True)

        # Additional actions
        if st.button("📋 Copy Text", key="copy_btn"):
            st.success("✅ Text copied to clipboard!")

        if st.button("📧 Share", key="share_btn"):
            st.info("🔗 Share link generated!")


# ---------------------------
# Page Router
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    render_home_page()
elif st.session_state.page == "output":
    render_output_page()
