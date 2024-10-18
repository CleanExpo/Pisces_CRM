import os
from google.cloud import speech
from google.cloud import vision
import cv2
import numpy as np
import spacy
from openai import OpenAI

# Initialize AI models
nlp = spacy.load("en_core_web_sm")

speech_client = speech.SpeechClient()
vision_client = vision.ImageAnnotatorClient()

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def process_input(data_type, data_content, inspection_context):
    if data_type == 'text':
        return process_text(data_content, inspection_context)
    elif data_type == 'audio':
        return process_audio(data_content, inspection_context)
    elif data_type == 'image':
        return process_image(data_content, inspection_context)
    elif data_type == 'video':
        return process_video(data_content, inspection_context)
    else:
        return "Unsupported data type"

def process_text(text, inspection_context):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    prompt = f"""
    Analyze the following text for a water damage inspection:

    Inspection Context:
    {inspection_context}

    Text Input:
    {text}

    Extracted Entities:
    {entities}

    Please provide:
    1. A detailed interpretation of the text in the context of water damage.
    2. Identify any potential issues or areas of concern.
    3. Suggest next steps or recommendations based on this information.
    4. Any additional insights that might be relevant for the inspection report.
    """
    
    interpretation = send_openai_request(prompt)
    return interpretation

def process_audio(audio_content, inspection_context):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = speech_client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript
    
    prompt = f"""
    Analyze the following transcript from a water damage inspection audio:

    Inspection Context:
    {inspection_context}

    Audio Transcript:
    {transcript}

    Please provide:
    1. A detailed interpretation of the audio content in the context of water damage.
    2. Identify any potential issues or areas of concern mentioned.
    3. Suggest next steps or recommendations based on this information.
    4. Any additional insights that might be relevant for the inspection report.
    5. If any measurements or specific damage descriptions are mentioned, highlight them.
    """
    
    interpretation = send_openai_request(prompt)
    return f"Transcript: {transcript}\n\nAI Interpretation: {interpretation}"

def process_image(image_content, inspection_context):
    image = vision.Image(content=image_content)
    response = vision_client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    
    # Perform text detection
    text_response = vision_client.text_detection(image=image)
    detected_text = text_response.text_annotations[0].description if text_response.text_annotations else "No text detected"
    
    prompt = f"""
    Analyze the following information from a water damage inspection image:

    Inspection Context:
    {inspection_context}

    Detected Labels:
    {', '.join(labels)}

    Detected Text in Image:
    {detected_text}

    Please provide:
    1. A detailed interpretation of the image content in the context of water damage.
    2. Identify any potential issues or areas of concern based on the labels and text.
    3. Suggest next steps or recommendations based on this visual information.
    4. Any additional insights that might be relevant for the inspection report.
    5. If any measurements or specific damage indicators are visible, highlight them.
    """
    
    interpretation = send_openai_request(prompt)
    return f"Detected labels: {', '.join(labels)}\nDetected text: {detected_text}\n\nAI Interpretation: {interpretation}"

def process_video(video_content, inspection_context):
    # For simplicity, we'll process the first frame of the video as an image
    nparr = np.frombuffer(video_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    _, buffer = cv2.imencode('.jpg', img)
    return process_image(buffer.tobytes(), inspection_context)

def send_openai_request(prompt: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert AI assistant specializing in water damage inspection and restoration. Provide detailed, accurate, and professional analyses of inspection data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("OpenAI returned an empty response.")
    return content

def generate_comprehensive_report(inspection_data, ssra_data, grid_map):
    prompt = f"""
    Generate a comprehensive water damage inspection report based on the following data:

    Inspection Data:
    {inspection_data}

    Site-Specific Risk Assessment (SSRA) Data:
    {ssra_data}

    Grid Map Data:
    {grid_map}

    Please provide:
    1. An executive summary of the inspection findings.
    2. Detailed analysis of each inspection step, including observations and AI interpretations.
    3. A risk assessment summary based on the SSRA data.
    4. Interpretation of the grid map data, highlighting areas of concern.
    5. Recommendations for remediation and next steps.
    6. Any additional insights or concerns that should be addressed.

    Format the report in a professional, easy-to-read structure suitable for both technicians and property owners.
    """
    
    report = send_openai_request(prompt)
    return report
