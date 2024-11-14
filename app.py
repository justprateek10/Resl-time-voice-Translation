from flask import Flask, render_template, request, jsonify
import whisper
from transformers import pipeline
import pyttsx3  # Import pyttsx3 for TTS

# Initialize the Flask app and models
app = Flask(__name__)

# Load Whisper for transcription
whisper_model = whisper.load_model("base")

# Load Hugging Face translation pipeline (Example: Translating English to French)
translator = pipeline("translation_en_to_fr")  # Translating English to French, adjust as needed

# Initialize the pyttsx3 TTS engine
engine = pyttsx3.init()

# Set the voice properties (male/female) and speaking speed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female, 0 for male
engine.setProperty('rate', 150)  # Adjust speaking speed

# Define the routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/translate', methods=['POST'])
def translate_audio():
    # Get audio file from the client
    audio = request.files['audio']
    audio.save("temp.wav")

    # Transcribe the audio using Whisper
    result = whisper_model.transcribe("temp.wav")
    transcribed_text = result["text"]

    # Translate the transcribed text
    translation = translator(transcribed_text)[0]['translation_text']

    # Speak the translation aloud using pyttsx3
    engine.say(translation)
    engine.runAndWait()

    # Return JSON response with transcription and translation
    return jsonify({
        "transcription": transcribed_text,
        "translation": translation
    })

if __name__ == '__main__':
    app.run(debug=True)
