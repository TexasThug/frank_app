# frank_core.py
import os
import requests
import openai
import re
import tempfile
import time
from pygame import mixer

# === Récupération des clés depuis les variables d'environnement ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ Attention : OPENAI_API_KEY non définie dans les variables d'environnement.")

# === CONFIG ===
#OPENAI_API_KEY = "sk-proj-XXXX"
#ELEVENLABS_API_KEY = "api-XXXX"
#WEATHER_API_KEY = "13d34352184f2a4fbe63a7f08b47171e"
openai.api_key = OPENAI_API_KEY

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # changeable

def speak(text):
    """Renvoie un fichier MP3 ElevenLabs temporaire"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text[:250],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(response.content)
    tmp.close()
    return tmp.name

def get_weather(city):
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

def detect_intent(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["météo", "temps", "degrés", "pluie", "fait-il"]):
        match = re.search(r"(?:à|a)\s+([a-zA-Zéèêàçûîôïäëù\-]+)", text_lower)
        city = match.group(1) if match else "Paris"
        return get_weather(city)
    elif "stop" in text_lower:
        return "stop"
    else:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-tts",
            messages=[
                {"role": "system", "content": "Tu es Frank, un assistant vocal chaleureux et positif."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
