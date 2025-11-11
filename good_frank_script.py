import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # cache le message pygame

import requests
import speech_recognition as sr
import openai
import datetime
import re
import time
import tempfile
from pygame import mixer

# === CONFIGURATION ===
#OPENAI_API_KEY = "sk-proj-XXXX"
#LEVENLABS_API_KEY = "api-XXXX"
#WEATHER_API_KEY = "13d34352184f2a4fbe63a7f08b47171e"
openai.api_key = OPENAI_API_KEY

# === PERSONNALITÉ ===
NAME = "Frank"
PERSONALITY = "chaleureux, bienveillant, complice et positif"

# === VOIX DISPONIBLES ===
VOICES = {
    "1": ("EXAVITQu4vr4xnSDxMaL", "Antoine (masculine, douce)"),
    "2": ("21m00Tcm4TlvDq8ikWAM", "Rachel (féminine, chaleureuse)"),
    "3": ("AZnzlk1XvdvUeBnXmlld", "Bella (féminine, jeune)"),
    "4": ("ErXwobaYiN019PkySvjV", "Elli (neutre, posée)")
}

def choose_voice():
    print("🎙️ Choisis la voix de Frank :")
    for key, (_, desc) in VOICES.items():
        print(f"  {key}. {desc}")
    choice = input("👉 Numéro de la voix : ").strip()
    return VOICES.get(choice, VOICES["1"])[0]

# Sélection au lancement
VOICE_ID = choose_voice()

# === VOIX ===
def speak(text):
    """Fait parler Frank avec ElevenLabs."""
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        text = text[:250]  # limite la taille pour rapidité

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.content)
            file_path = f.name

        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()

        while mixer.music.get_busy():
            time.sleep(0.1)

        mixer.music.unload()
        os.remove(file_path)

    except Exception as e:
        print("Erreur ElevenLabs :", e)

# === MÉTÉO ===
def get_weather(city):
    #url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=fr"
    try:
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
        return f"Je n'ai pas réussi à récupérer la météo ({e})."

# === INTENT DETECTION ===
def detect_intent(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["météo", "temps", "degrés", "pluie", "fait-il"]):
        match = re.search(r"(?:à|a)\s+([a-zA-Zéèêàçûîôïäëù\-]+)", text_lower)
        city = match.group(1) if match else "Paris"
        return get_weather(city)
    elif "stop" in text_lower or "au revoir" in text_lower:
        return "stop"
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini-tts",
                messages=[
                    {"role": "system", "content": f"Tu es {NAME}, un assistant vocal {PERSONALITY}."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Je ne peux pas répondre pour le moment ({e})."

# === MAIN LOOP ===
r = sr.Recognizer()
print("🎧 Frank est à l’écoute. Dis 'Frank' pour lui parler, ou 'stop' pour quitter.")

while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("En attente du mot-clé 'Frank'...")
        audio = r.listen(source)

    try:
        trigger = r.recognize_google(audio, language="fr-FR").lower()
        if "frank" in trigger or "franck" in trigger:
            print("Oui ? Je t’écoute...")
            speak("Oui ? Je t’écoute...")

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("J'écoute ta question...")
                audio = r.listen(source)

            phrase = r.recognize_google(audio, language="fr-FR")
            print("Tu as dit :", phrase)

            reponse = detect_intent(phrase)
            if reponse == "stop":
                speak("À bientôt !")
                break

            print(f"{NAME} :", reponse)
            speak(reponse)
            time.sleep(0.5)

    except sr.UnknownValueError:
        continue
    except Exception as e:
        print("Erreur :", e)
        time.sleep(1)
