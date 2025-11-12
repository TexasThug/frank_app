import os
import requests
import openai
import re
import tempfile
import traceback
from dotenv import load_dotenv

# === Chargement des variables d'environnement ===
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️  Clé OpenAI manquante. Vérifie ton fichier .env.")
if not ELEVENLABS_API_KEY:
    print("⚠️  Clé ElevenLabs manquante. Vérifie ton fichier .env.")
if not WEATHER_API_KEY:
    print("⚠️  Clé Météo manquante. Vérifie ton fichier .env.")

openai.api_key = OPENAI_API_KEY

# === Config voix ElevenLabs ===
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # voix féminine douce


# === Fonction Text-To-Speech (TTS) ===
def speak(text):
    """Génère un fichier MP3 avec ElevenLabs et le stocke dans /static/audio pour que Flask puisse le servir"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:250],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.85}
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    # 📁 Nouveau chemin : Frank_App/static/audio
    audio_folder = os.path.join(os.getcwd(), "static", "audio")
    os.makedirs(audio_folder, exist_ok=True)

    # 🧠 Nom unique du fichier
    filename = next(tempfile._get_candidate_names()) + ".mp3"
    file_path = os.path.join(audio_folder, filename)

    # 💾 Sauvegarde dans static/audio/
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"🎵 Fichier audio généré et stocké ici : {file_path}")
    return file_path

# === Fonction météo ===
def get_weather(city):
    """Retourne la météo actuelle pour une ville"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=fr"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return f"Je ne trouve pas la météo pour {city}."

        temp = round(data["main"]["temp"])
        desc = data["weather"][0]["description"]
        phrase = (
            "le ciel est un peu gris" if "nuage" in desc else
            "il pleut un peu, pense à prendre un parapluie" if "pluie" in desc else
            "le soleil brille, profite bien" if "soleil" in desc else
            f"le temps est {desc}"
        )
        return f"À {city.capitalize()}, il fait environ {temp} degrés, et {phrase}."

    except Exception as e:
        print("🚨 Erreur météo :", e)
        traceback.print_exc()
        return "Je ne parviens pas à obtenir la météo pour le moment."


# === Fonction principale : détection d’intention ===
def detect_intent(text):
    """Analyse la phrase et renvoie la bonne réponse"""
    try:
        text_lower = text.lower()

        # 1️⃣ — Demande météo
        if any(w in text_lower for w in ["météo", "temps", "degrés", "pluie", "fait-il"]):
            match = re.search(r"(?:à|a)\s+([a-zA-Zéèêàçûîôïäëù\-]+)", text_lower)
            city = match.group(1) if match else "Paris"
            return get_weather(city)

        # 2️⃣ — Arrêt
        elif "stop" in text_lower:
            return "D’accord, j’arrête d’écouter."

        # 3️⃣ — Réponse IA
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Tu es Good Frank, un assistant vocal bienveillant, clair et chaleureux. "
                            "Tu réponds en français, en une ou deux phrases maximum, "
                            "et avec un ton calme et rassurant."
                        )
                    },
                    {"role": "user", "content": text}
                ]
            )
            reply = response.choices[0].message.content.strip()
            print(f"🤖 Réponse IA : {reply}")
            return reply

    except Exception as e:
        print("🚨 Erreur detect_intent :", e)
        traceback.print_exc()
        return "Désolé, j’ai un petit souci technique."
