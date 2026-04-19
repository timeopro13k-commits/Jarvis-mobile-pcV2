# Config.py

import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class AudioConfig:
sample_rate: int = 44100
channels: int = 1
chunk_size: int = 1024
clap_threshold: float = 0.35
clap_min_interval: float = 0.1
clap_max_interval: float = 0.6
clap_cooldown: float = 1.5

@dataclass
class AIConfig:
# Mettez votre clé OpenRouter ici (gratuite sur openrouter.ai)
api_key: str = “api_key: str = "sk-or-v1-7c810ca492c02-fec4d2c27e4366d210e7bf4a7d802551a2a43a237b0a02748cd"
”
base_url: str = “https://openrouter.ai/api/v1”
model: str = “meta-llama/llama-4-scout:free”
personality: str = (
“Tu es JARVIS, un assistant IA élégant et légèrement sarcastique. “
“Tu réponds en français en 1-2 phrases maximum.”
)
max_tokens: int = 300

@dataclass
class SpeechConfig:
stt_engine: str = “whisper”
whisper_model: str = “base”
tts_engine: str = “pyttsx3”
tts_rate: int = 175
tts_volume: float = 0.9

@dataclass
class SecurityConfig:
allowed_apps: List[str] = field(default_factory=lambda: [
“chrome”, “firefox”, “safari”, “edge”,
“code”, “vscode”,
“terminal”, “cmd”, “powershell”,
“finder”, “explorer”,
“spotify”, “vlc”,
“calculator”, “notepad”,
])
require_confirmation: List[str] = field(default_factory=lambda: [
“rm”, “del”, “format”, “shutdown”, “reboot”,
])
log_file: str = “jarvis.log”

@dataclass
class ServerConfig:
host: str = “localhost”
port: int = 8765

@dataclass
class JarvisConfig:
audio: AudioConfig = field(default_factory=AudioConfig)
ai: AIConfig = field(default_factory=AIConfig)
speech: SpeechConfig = field(default_factory=SpeechConfig)
security: SecurityConfig = field(default_factory=SecurityConfig)
server: ServerConfig = field(default_factory=ServerConfig)
name: str = “JARVIS”

CONFIG = JarvisConfig()
