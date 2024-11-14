from flask import Flask, render_template, request, jsonify
import whisper
from transformers import pipeline
import pyttsx3  # Import pyttsx3 for TTS

# Initialize the Flask app and models
app = Flask(__name__)

# Load Whisper for transcription
whisper_model = whisper.load_model("base")

# Initialize the pyttsx3 TTS engine
engine = pyttsx3.init()

# Set the voice properties (male/female) and speaking speed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0.id)  # 1 for female, 0 for male
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

    # Get the target language from the client (e.g., from form data or query)
    target_language = request.form.get('target_language', 'fr')  # Default to French

    # Dynamically load the translation pipeline based on the target language
    translation_pipeline = pipeline(f"translation_en_to_{target_language}")

    # Translate the transcribed text
    translation = translation_pipeline(transcribed_text)[0]['translation_text']

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
