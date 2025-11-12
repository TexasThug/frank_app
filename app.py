# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from frank_core import detect_intent, speak
import os
import traceback

# === CONFIGURATION FLASK ===
app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)

# Autoriser le front (Render / HTTPS / localhost) à communiquer avec le backend
CORS(app)

# === PAGE D’ACCUEIL ===
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        print("⚠️ Erreur affichage page :", e)
        traceback.print_exc()
        return "Erreur chargement de la page", 500


# === ROUTE DE DISCUSSION ===
@app.route("/ask", methods=["POST"])
def ask_frank():
    try:
        data = request.get_json()
        user_text = data.get("text", "")

        print(f"👤 Utilisateur : {user_text}")

        # 🔍 Analyse de l’intention (GPT ou météo)
        response_text = detect_intent(user_text)
        print(f"🤖 Frank : {response_text}")

        # 🎧 Génère la réponse vocale
        audio_path = speak(response_text)

        if not audio_path:
            return jsonify({
                "response_text": response_text,
                "audio_url": None,
                "error": "Erreur génération audio"
            })

        return jsonify({
            "response_text": response_text,
            "audio_url": f"/audio/{os.path.basename(audio_path)}"
        })

    except Exception as e:
        print("🚨 Erreur dans /ask :", e)
        traceback.print_exc()
        return jsonify({"error": "Erreur serveur"}), 500


# === ROUTE POUR L’AUDIO ===
@app.route("/audio/<filename>")
def get_audio(filename):
    try:
        file_path = os.path.join("static", "audio", filename)
        if not os.path.exists(file_path):
            print(f"⚠️ Audio introuvable : {file_path}")
            return jsonify({"error": "Audio non trouvé"}), 404

        # Lecture directe sans téléchargement
        return send_file(file_path, mimetype="audio/mpeg", as_attachment=False, conditional=False)

    except Exception as e:
        print("🚨 Erreur lecture audio :", e)
        traceback.print_exc()
        return jsonify({"error": "Erreur serveur audio"}), 500


# === FICHIERS PWA ===
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")


# === LANCEMENT DU SERVEUR ===
if __name__ == "__main__":
    # ✅ Render attribue un port dynamique → on le récupère
    port = int(os.environ.get("PORT", 5000))

    print(f"🚀 Démarrage de Good Frank sur le port {port}")
    print("🌐 Accessible sur Render et en local (0.0.0.0)")

    app.run(host="0.0.0.0", port=port, debug=True)
