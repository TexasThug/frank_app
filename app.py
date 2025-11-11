# app.py
from flask import Flask, request, jsonify, send_file
from frank_core import detect_intent, speak
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Frank API en ligne. Utilise /ask pour discuter."

@app.route("/ask", methods=["POST"])
def ask_frank():
    data = request.get_json()
    user_text = data.get("text", "")

    print(f"👤 Utilisateur : {user_text}")
    response_text = detect_intent(user_text)
    print(f"🤖 Frank : {response_text}")

    # Génère la réponse vocale
    audio_path = speak(response_text)

    return jsonify({
        "response_text": response_text,
        "audio_url": f"/audio/{os.path.basename(audio_path)}"
    })

@app.route("/audio/<filename>")
def get_audio(filename):
    file_path = os.path.join("/tmp", filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Audio non trouvé"}), 404
    return send_file(file_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
