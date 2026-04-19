# Jarvis-mobile-pcV2
Using openrooter 
# JARVIS — Assistant IA Desktop

> *“Bonjour. Tous les systèmes sont opérationnels.”*

Assistant vocal et textuel futuriste, activable par double claquement de mains, avec interface WebGL animée et IA via OpenRouter.

-----

## Fichiers du projet

```
jarvis-pc/
├── Config.py          # Configuration (clé OpenRouter, modèle, etc.)
├── AI_engine.py       # Moteur IA — OpenRouter + patterns offline
├── Clap_detector.py   # Détection double clap
├── Audio_engine.py    # Capture microphone en continu
├── Commander.py       # Lancement d'applications sécurisé
├── Main.py            # Serveur principal WebSocket
├── Index.html         # Interface futuriste WebGL
├── Start.sh           # Script de démarrage
└── requirements.txt   # Dépendances Python
```

-----

## Installation

### 1. Cloner le repo

```bash
git clone https://github.com/vous/jarvis-mobile-pcV2.git
cd jarvis-mobile-pcV2
```

### 2. Obtenir une clé OpenRouter (gratuit, sans CB)

1. Allez sur **openrouter.ai**
1. **Sign in** avec Google ou GitHub
1. **Keys** → **Create Key**
1. Copiez la clé (`sk-or-v1-...`)

### 3. Coller la clé dans Config.py

Ouvrez `Config.py` et remplacez :

```python
api_key: str = "
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"
```

par votre vraie clé :

```python
api_key: str = "sk-or-v1-xxxxxxxxxxxx"
```

### 4. Lancer JARVIS

```bash
chmod +x Start.sh
./Start.sh
```

C’est tout. Le script installe les dépendances et démarre automatiquement.

-----

## Utilisation

### Activation par double clap

Claquements des mains deux fois rapidement. L’orbe passe au vert, JARVIS écoute.

### Commandes vocales

```
"Lance Chrome"
"Ouvre Firefox"
"Quelle heure est-il ?"
"Infos système"
"Calcule 15 fois 8"
"Raconte une blague"
"Au revoir"
```

### Mode texte

Tapez directement dans le champ en bas de l’interface.

### Simulation sans micro

Cliquez sur l’orbe central pour simuler un double clap.

-----

## Configuration

Tout se passe dans `Config.py` :

### Changer de modèle IA (tous gratuits)

```python
model: str = "meta-llama/llama-4-scout:free"      # Défaut — très bon
model: str = "mistralai/mistral-7b-instruct:free"  # Plus léger
model: str = "deepseek/deepseek-r1:free"           # Meilleur en raisonnement
model: str = "google/gemma-3-12b-it:free"          # Google Gemma
```

### Changer la personnalité

```python
personality: str = "Tu es JARVIS, sarcastique et efficace. Tu appelles l'utilisateur patron."
```

### Changer la sensibilité des claps

```python
clap_threshold: float = 0.35   # 0.1 = très sensible / 0.9 = peu sensible
clap_max_interval: float = 0.6 # Secondes max entre les 2 claps
```

### Ajouter des applications autorisées

```python
allowed_apps: List[str] = field(default_factory=lambda: [
    "chrome", "firefox", "spotify", "discord", ...
])
```

-----

## Dépendances

|Package                |Rôle                             |
|-----------------------|---------------------------------|
|`fastapi` + `uvicorn`  |Serveur WebSocket                |
|`sounddevice` + `numpy`|Capture micro et traitement audio|
|`httpx`                |Appels API OpenRouter            |
|`pyttsx3`              |Synthèse vocale offline          |
|`openai-whisper`       |Reconnaissance vocale offline    |
|`psutil`               |Infos CPU / RAM                  |

-----

## Problèmes courants

**Le micro n’est pas détecté**

```bash
python3 -c "import sounddevice; print(sounddevice.query_devices())"
```

Vérifiez que votre micro est le périphérique par défaut.

**Whisper télécharge un modèle au premier lancement**
Normal — le modèle `base` (~150 Mo) est téléchargé une seule fois.

**Les claps ne sont pas détectés**
Réduisez `clap_threshold` à `0.2` dans `Config.py`.

**L’IA ne répond pas**
Vérifiez que votre clé dans `Config.py` commence bien par `sk-or-v1-`.

-----

## Licence

MIT — Libre d’utilisation et de modification.
