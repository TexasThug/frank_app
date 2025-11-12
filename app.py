# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from frank_core import detect_intent, speak
import os

# === CONFIGURATION FLASK ===
app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)

# === PAGE D’ACCUEIL ===
@app.route("/")
def home():
    # 👉 Cette ligne sert à afficher ton interface index.html
    return render_template("index.html")


# === ROUTE DE DISCUSSION ===
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


# === ROUTE POUR L’AUDIO ===
@app.route("/audio/<filename>")
def get_audio(filename):
    file_path = os.path.join("static", "audio", filename)
    if not os.path.exists(file_path):
        print(f"⚠️ Audio introuvable : {file_path}")
        return jsonify({"error": "Audio non trouvé"}), 404
    return send_file(file_path, mimetype="audio/mpeg")


# === FICHIERS PWA ===
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")


# === LANCEMENT DU SERVEUR ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
