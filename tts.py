# tts_runner.py
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# --- IBM TTS setup ---
# Removed global API_KEY and tts_service
URL = "https://api.eu-de.text-to-speech.watson.cloud.ibm.com"


# English voice options
ENGLISH_VOICES = {
    # US English - Standard
    "allison": "en-US_AllisonV3Voice",
    "lisa": "en-US_LisaV3Voice",
    "michael": "en-US_MichaelV3Voice",
    "kevin": "en-US_KevinV3Voice",
    "henry": "en-US_HenryV3Voice",
    "emily": "en-US_EmilyV3Voice",

    # US English - Expressive (supports emotions)
    "allison_expressive": "en-US_AllisonExpressive",
    "emma_expressive": "en-US_EmmaExpressive",
    "lisa_expressive": "en-US_LisaExpressive",
    "michael_expressive": "en-US_MichaelExpressive",

    # British English
    "kate_british": "en-GB_KateV3Voice",
    "charlotte_british": "en-GB_CharlotteV3Voice",
    "james_british": "en-GB_JamesV3Voice",

    # Australian English
    "heidi_australian": "en-AU_HeidiExpressive",
    "jack_australian": "en-AU_JackExpressive",
}

# Emotion mapping to SSML expressions
EMOTION_MAPPING = {
    'ANGRY': 'angry',
    'DISGUST': 'disgusted',
    'FEAR': 'afraid',
    'HAPPY': 'cheerful',
    'JOY': 'cheerful',
    'SAD': 'sad',
    'SURPRISE': 'surprised',
    'NEUTRAL': 'neutral',
    'EXCITED': 'excited',
    'CALM': 'calm'
}


def get_voice_info(voice_name):
    """Get information about a voice."""
    voice = ENGLISH_VOICES.get(voice_name, "")

    info = {
        'supports_emotions': 'Expressive' in voice,
        'gender': 'Female' if any(name in voice for name in ['Allison', 'Lisa', 'Emily', 'Emma', 'Kate', 'Charlotte', 'Heidi']) else 'Male',
        'accent': 'British' if 'GB' in voice else 'Australian' if 'AU' in voice else 'American',
        'voice_id': voice
    }

    return info


def generate_tts(
    emotion_objects,
    output_file="output_audio.mp3",
    voice_name="allison_expressive",
    api_key=None,
):
    """
    Convert text with emotions to speech and save as a single audio file.

    Args:
        emotion_objects: List of dicts containing 'speech_text' and 'emotion' keys.
        output_file: Path to save the audio file.
        voice_name: Voice name from ENGLISH_VOICES keys (default: allison_expressive).
        api_key: IBM Cloud API Key.

    Returns:
        Path to the saved audio file.
    """
    if not api_key:
        raise ValueError("API Key is required for TTS generation.")

    authenticator = IAMAuthenticator(api_key)
    tts_service = TextToSpeechV1(authenticator=authenticator)
    tts_service.set_service_url(URL)

    # Get actual voice ID from friendly name
    voice = ENGLISH_VOICES.get(voice_name, "en-US_AllisonExpressive")
    is_expressive = "Expressive" in voice
    voice_info = get_voice_info(voice_name)

    print(f"Using voice: {voice_name} ({voice})")
    print(f"Voice info: {voice_info}")

    if is_expressive:
        # Build SSML with emotions for expressive voices
        ssml_parts = ['<speak>']

        for obj in emotion_objects:
            text = obj["speech_text"]
            emotion = obj.get("emotion", "NEUTRAL").upper()

            # Map emotion to SSML expression
            ssml_emotion = EMOTION_MAPPING.get(emotion, "neutral")

            # Create enhanced SSML with emotion and prosody
            if emotion == 'ANGRY':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="fast" pitch="+20%">{text}</prosody></express-as>'
            elif emotion == 'SAD':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="slow" pitch="-15%">{text}</prosody></express-as>'
            elif emotion == 'HAPPY' or emotion == 'JOY':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="medium" pitch="+10%">{text}</prosody></express-as>'
            elif emotion == 'FEAR':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="fast" pitch="+25%">{text}</prosody></express-as>'
            elif emotion == 'SURPRISE':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="fast" pitch="+20%">{text}</prosody></express-as>'
            elif emotion == 'DISGUST':
                ssml_part = f'<express-as type="{ssml_emotion}"><prosody rate="slow" pitch="-10%">{text}</prosody></express-as>'
            else:
                # Neutral and other emotions
                ssml_part = f'<express-as type="{ssml_emotion}">{text}</express-as>'

            # Add pause between sentences
            ssml_part += '<break time="0.8s"/>'

            ssml_parts.append(ssml_part)

        ssml_parts.append('</speak>')
        synthesis_text = ''.join(ssml_parts)

        print(f"Generated SSML: {synthesis_text[:300]}...")  # Debug print

    else:
        # Use simple text concatenation for standard voices
        synthesis_text = ". ".join([obj["speech_text"]
                                   for obj in emotion_objects])
        print(f"Using standard voice - no emotion support")

    try:
        # Generate audio
        response = tts_service.synthesize(
            synthesis_text,
            voice=voice,
            accept="audio/mp3"
        ).get_result()

        with open(output_file, "wb") as audio_file:
            audio_file.write(response.content)

        print(f"✅ Audio successfully generated with {voice_name}")

    except Exception as e:
        print(f"❌ Error with {voice_name} voice: {e}")
        print("🔄 Falling back to basic synthesis...")

        try:
            # Fallback: use basic voice without emotions
            combined_text = ". ".join([obj["speech_text"]
                                      for obj in emotion_objects])
            response = tts_service.synthesize(
                combined_text,
                voice="en-US_AllisonV3Voice",
                accept="audio/mp3"
            ).get_result()

            with open(output_file, "wb") as audio_file:
                audio_file.write(response.content)

            print("✅ Audio generated with fallback voice")

        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            raise

    print(f"🎵 Audio saved as {output_file}")
    return output_file


def list_available_voices():
    """Display all available English voice options with detailed info."""
    print("\n" + "="*60)
    print("🎤 AVAILABLE ENGLISH VOICES")
    print("="*60)

    print("\n🇺🇸 US English (Standard Voices):")
    print("-" * 40)
    for key, voice in ENGLISH_VOICES.items():
        if "en-US" in voice and "Expressive" not in voice:
            info = get_voice_info(key)
            print(f"  • {key:<20} | {info['gender']:<6} | Clear narration")

    print("\n🎭 US English (Expressive Voices - Support Emotions):")
    print("-" * 55)
    for key, voice in ENGLISH_VOICES.items():
        if "en-US" in voice and "Expressive" in voice:
            info = get_voice_info(key)
            print(
                f"  • {key:<20} | {info['gender']:<6} | Full emotion support")

    print("\n🇬🇧 British English:")
    print("-" * 25)
    for key, voice in ENGLISH_VOICES.items():
        if "en-GB" in voice:
            info = get_voice_info(key)
            print(f"  • {key:<20} | {info['gender']:<6} | British accent")

    print("\n🇦🇺 Australian English:")
    print("-" * 28)
    for key, voice in ENGLISH_VOICES.items():
        if "en-AU" in voice:
            info = get_voice_info(key)
            print(
                f"  • {key:<20} | {info['gender']:<6} | Australian accent + emotions")

    print("\n" + "="*60)
    print("📝 EMOTION SUPPORT:")
    print("   Expressive voices support: " + ", ".join(EMOTION_MAPPING.keys()))
    print("="*60)


def test_voice(voice_name, test_text="Hello, this is a test of the text to speech system."):
    """Test a specific voice with sample text."""
    print(f"\n🧪 Testing voice: {voice_name}")

    if voice_name not in ENGLISH_VOICES:
        print(f"❌ Voice '{voice_name}' not found!")
        return False

    test_objects = [{"speech_text": test_text, "emotion": "NEUTRAL"}]
    test_file = f"test_{voice_name}.mp3"

    try:
        generate_tts(test_objects, test_file, voice_name)
        print(f"✅ Test successful! Audio saved as {test_file}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def get_recommended_voice(content_type="story"):
    """Get recommended voice based on content type."""
    recommendations = {
        "story": "allison_expressive",
        "professional": "michael_expressive",
        "casual": "kevin",
        "dramatic": "lisa_expressive",
        "british": "james_british",
        "energetic": "emily",
        "mature": "henry"
    }

    return recommendations.get(content_type, "allison_expressive")


# Usage examples and testing
if __name__ == "__main__":
    # Display available voices
    list_available_voices()

    # Test sample
    sample_emotions = [
        {"speech_text": "Hello everyone, welcome to this story.", "emotion": "HAPPY"},
        {"speech_text": "Suddenly, something terrible happened!", "emotion": "FEAR"},
        {"speech_text": "But in the end, everything worked out perfectly.", "emotion": "JOY"}
    ]

    # Test with different voices
    print("\n🧪 Running voice tests...")
    test_voice("allison_expressive")
    test_voice("michael")
    test_voice("james_british")
