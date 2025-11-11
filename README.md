# 🧠 Frank Assistant — L’agent vocal bienveillant pour les seniors

> **Frank** est un assistant vocal conçu pour **aider les personnes âgées au quotidien**, leur rappeler leurs rendez-vous, les encourager et leur tenir compagnie.  
> Il s’inspire d’Alexa ou Siri, mais avec une **voix plus humaine, douce et rassurante**.

---

## 🚀 Fonctionnalités principales

- 🎙️ Reconnaissance vocale naturelle (via SpeechRecognition)
- 💬 Réponses intelligentes et bienveillantes (OpenAI API)
- 🔔 Rappels personnalisés et météo locale
- 🔉 Voix réaliste grâce à ElevenLabs
- 🧩 Interface API Flask prête à être connectée à une application mobile

---

## 🧰 Stack Technique

- **Langage** : Python 3  
- **Framework** : Flask  
- **IA** : OpenAI GPT  
- **Voix** : ElevenLabs (TTS API)  
- **Déploiement** : Render  

---

## ⚙️ Installation locale

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/TexasThug/Frank_assistant.git
cd Frank_assistant

2️⃣ Créer un environnement virtuel

python -m venv venv
source venv/bin/activate  # sur macOS/Linux
venv\Scripts\activate     # sur Windows

3️⃣ Installer les dépendances
pip install -r requirements.txt

4️⃣ Créer un fichier .env

Crée un fichier à la racine du projet :

OPENAI_API_KEY=ta_clé_openai
ELEVENLABS_API_KEY=ta_clé_elevenlabs


(⚠️ Ce fichier n’est pas poussé sur GitHub pour des raisons de sécurité.)

5️⃣ Lancer le serveur local
python app.py


Frank sera alors accessible sur :
👉 http://localhost:5000

🌐 Déploiement en ligne (Render)

L’application est hébergée sur Render :
👉 https://frank-assistant.onrender.com

Chaque fois que vous poussez une mise à jour sur GitHub (git push), Render déploie automatiquement la nouvelle version.

👥 Équipe

Projet réalisé dans le cadre du Hackathon M2 IA & Business
Contributeurs :

🧑‍💻 TexasThug — Développeur principal

👩‍💻 Équipe IA & UX — Idéation, tests et scénarios utilisateur

💡 Vision long terme

Frank deviendra un compagnon de vie connecté :

capable d’analyser l’humeur quotidienne via la voix,

d’envoyer un bilan journalier à la famille,

et de prévenir les proches en cas d’anomalie détectée.

🤍 « Frank veille sur vous, comme un ami. »
