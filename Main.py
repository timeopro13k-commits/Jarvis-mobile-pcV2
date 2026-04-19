# Main.py

import asyncio
import json
import logging
import time
import sys
from pathlib import Path

logging.basicConfig(
level=logging.INFO,
format=’%(asctime)s [%(name)s] %(levelname)s: %(message)s’,
handlers=[
logging.StreamHandler(sys.stdout),
logging.FileHandler(“jarvis.log”, encoding=‘utf-8’),
]
)
logger = logging.getLogger(“jarvis”)

sys.path.insert(0, str(Path(**file**).parent))

from Config        import CONFIG
from Clap_detector import ClapDetector
from Audio_engine  import AudioEngine
from Commander     import Commander
from AI_engine     import AIEngine

try:
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
except ImportError:
logger.error(“Lancez : pip install fastapi uvicorn”)
sys.exit(1)

app       = FastAPI(title=“JARVIS”)
clap      = ClapDetector(CONFIG.audio)
commander = Commander(CONFIG)
ai        = AIEngine(CONFIG)
audio     = None
clients   = []

# ── WebSocket ─────────────────────────────────────────────────────────────────

async def broadcast(msg: dict):
dead = []
for c in clients:
try: await c.send_text(json.dumps(msg))
except: dead.append(c)
for c in dead: clients.remove(c)

async def status(s: str, data: dict = None):
await broadcast({“type”: “status”, “status”: s, “data”: data or {}, “ts”: time.time()})

async def speak(text: str):
logger.info(f”JARVIS: {text}”)
await broadcast({“type”: “speak”, “text”: text})

# ── Logique ───────────────────────────────────────────────────────────────────

def on_clap():
asyncio.run_coroutine_threadsafe(wake(), asyncio.get_event_loop())

async def wake():
await status(“waking”)
await speak(“Je vous écoute.”)
if audio: audio.activate_voice_listening()
await status(“listening”)

def on_level(level: float):
asyncio.run_coroutine_threadsafe(
broadcast({“type”: “audio_level”, “level”: level}),
asyncio.get_event_loop()
)

async def handle_command(text: str):
await status(“processing”, {“command”: text})
intent = await ai.process(text)
msg = intent.response

```
if intent.action == "launch_app" and intent.target:
    r = await commander.launch_app(intent.target)
    if not r.success: msg = f"Impossible : {r.error}"
    else: await status("action", {"target": intent.target})

elif intent.action == "system_info":
    info = await commander.get_system_info()
    if info: msg = f"CPU {info['cpu_percent']}%, RAM {info['memory']['percent']}%."

elif intent.action == "open_file" and intent.target:
    r = await commander.open_file(intent.target)
    if not r.success: msg = r.error

elif intent.action == "quit":
    await speak("À bientôt.")
    await status("sleeping")
    return

await speak(msg)
await status("idle", {"response": msg})
```

# ── WebSocket endpoint ────────────────────────────────────────────────────────

@app.websocket(”/ws”)
async def ws(websocket: WebSocket):
await websocket.accept()
clients.append(websocket)
await websocket.send_text(json.dumps({
“type”: “init”, “status”: “ready”, “name”: CONFIG.name
}))
try:
while True:
msg = json.loads(await websocket.receive_text())
t = msg.get(“type”)
if t == “text_command”:
text = msg.get(“text”, “”).strip()
if text: await handle_command(text)
elif t == “simulate_clap”:
await wake()
elif t == “ping”:
await broadcast({“type”: “pong”})
except WebSocketDisconnect:
if websocket in clients: clients.remove(websocket)
except Exception as e:
logger.error(f”WS erreur: {e}”)
if websocket in clients: clients.remove(websocket)

# ── Démarrage ─────────────────────────────────────────────────────────────────

@app.on_event(“startup”)
async def startup():
global audio
logger.info(”=” * 40)
logger.info(”  JARVIS — Démarrage”)
logger.info(”=” * 40)

```
clap.on_double_clap(on_clap)
audio = AudioEngine(CONFIG, clap, None)
audio.on_audio_level(on_level)

def cmd_handler(text):
    asyncio.run_coroutine_threadsafe(handle_command(text), asyncio.get_event_loop())

audio.on_command(cmd_handler)

loop = asyncio.get_event_loop()
await loop.run_in_executor(None, audio.start)
logger.info(f"Prêt → ws://localhost:{CONFIG.server.port}/ws")
```

@app.on_event(“shutdown”)
async def shutdown():
if audio: audio.stop()

@app.get(”/health”)
async def health():
return {“status”: “ok”}

if **name** == “**main**”:
uvicorn.run(app, host=CONFIG.server.host, port=CONFIG.server.port, log_level=“warning”)
