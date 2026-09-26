"""
Text-to-Speech (TTS) module for MediScript.
Converts Tamil text instructions into audio files using gTTS.
"""

import os
from gtts import gTTS


def generate_tamil_audio(text: str, output_path: str = "temp_instruction.mp3") -> str:
    """
    Generates a Tamil MP3 audio file from text.
    
    :param text: Tamil plain text instruction.
    :param output_path: Destination path for the generated MP3 file.
    :return: File path to the generated MP3 file.
    """
    if not text or not text.strip():
        text = "மருந்து சீட்டு தகவல்கள் கிடைக்கவில்லை."

    tts = gTTS(text=text, lang='ta', slow=False)
    tts.save(output_path)
    return output_path