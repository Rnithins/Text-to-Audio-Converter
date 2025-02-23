from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import os
import time

app = Flask(__name__)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_text_to_audio():
    data = request.get_json()
    text = data.get('text', '').strip()
    language = data.get('language', 'en')
    slow = data.get('slow', False)

    if not text:
        return jsonify({'error': 'Please enter some text!'}), 400

    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        timestamp = str(int(time.time()))  # Unique filename
        audio_file = f"static/audio_{timestamp}.mp3"
        tts.save(audio_file)

        return jsonify({'audio_url': audio_file})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download Audio
@app.route('/download/<filename>')
def download_audio(filename):
    return send_file(f"static/{filename}", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
