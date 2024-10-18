import streamlit as st
from google.cloud import speech
import io
import cv2
import numpy as np
from PIL import Image

def input_form():
    st.subheader("Data Input")
    
    input_type = st.radio("Select input type", ["Text", "Speech", "Image", "Video"])
    
    if input_type == "Text":
        text_input = st.text_area("Enter description")
        if st.button("Submit Text"):
            return {"type": "text", "data": text_input}
    
    elif input_type == "Speech":
        audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
        if audio_file and st.button("Transcribe"):
            text = transcribe_audio(audio_file)
            st.write("Transcribed text:", text)
            return {"type": "speech", "data": text}
    
    elif input_type == "Image":
        image_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
        if image_file and st.button("Process Image"):
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            # Process image here (e.g., extract text, analyze damage)
            return {"type": "image", "data": image_file.getvalue()}
    
    elif input_type == "Video":
        video_file = st.file_uploader("Upload video", type=["mp4", "mov"])
        if video_file and st.button("Process Video"):
            # Process video here (e.g., extract frames, analyze damage over time)
            return {"type": "video", "data": video_file.getvalue()}
    
    return None

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    response = client.recognize(config=config, audio=audio)
    
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    
    return transcript
