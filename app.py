from flask import Flask, request, jsonify, render_template

import chat
import os
from gtts import gTTS
from io import BytesIO
import base64
import speech_recognition as sr
app = Flask(__name__)


import json
import re
import requests


@app.route('/')
def homepage():
    return render_template('index.html')
from flask import Flask, request, jsonify

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.get_json()['message']
    response = chat.process_text(message)
    print(response)

    # Check if voice input button was clicked
    if 'voice_input' in request.get_json():
        audio_input = get_audio()
    else:
        audio_input = None

    # Convert text to speech and encode as base64
    tts = gTTS(response)
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    encoded_audio = base64.b64encode(audio_stream.read()).decode('utf-8')

    return jsonify({'message': response, 'audio': encoded_audio, 'audio_input': audio_input})

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception:
            print("Exception")

    return said

if __name__ == '__main__':
    app.run(debug=True)
