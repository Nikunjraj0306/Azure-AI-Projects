import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Speech Credentials
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")


# --------------------------------
# Voice Mapping
# --------------------------------
VOICE_MAP = {
    "en-US": "en-US-JennyNeural",
    "hi-IN": "hi-IN-SwaraNeural",
    "fr-FR": "fr-FR-DeniseNeural",
    "de-DE": "de-DE-KatjaNeural",
    "es-ES": "es-ES-ElviraNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "ko-KR": "ko-KR-SunHiNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural"
}


# --------------------------------
# Text To Speech
# --------------------------------
def text_to_speech(text, language="en-US", output_path=None):
    """
    Convert text into speech audio file
    """

    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY,
            region=SPEECH_REGION
        )

        # Set voice
        voice_name = VOICE_MAP.get(
            language,
            "en-US-JennyNeural"
        )

        speech_config.speech_synthesis_voice_name = voice_name

        # Save audio
        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=output_path
        )

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return output_path

        raise Exception("Speech synthesis failed.")

    except Exception as e:
        raise Exception(f"TTS Error: {str(e)}")


# --------------------------------
# Speech To Text
# --------------------------------
def speech_to_text(language="en-US"):
    """
    Convert speech from microphone into text
    """

    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY,
            region=SPEECH_REGION
        )

        speech_config.speech_recognition_language = language

        audio_config = speechsdk.audio.AudioConfig(
            use_default_microphone=True
        )

        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        print("Speak something...")

        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text

        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech detected."

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            return f"Speech cancelled: {cancellation.reason}"

        return "Could not recognize speech."

    except Exception as e:
        return f"Speech Recognition Error: {str(e)}"