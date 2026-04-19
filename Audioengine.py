# Audio_engine.py

import threading
import logging
import time
import numpy as np
from typing import Callable, Optional

logger = logging.getLogger(“jarvis.audio”)

class AudioEngine:
def **init**(self, config, clap_detector, speech_engine):
self.cfg = config
self.clap = clap_detector
self.speech = speech_engine
self._running = False
self._listening = False
self._thread: Optional[threading.Thread] = None
self._on_wake: Optional[Callable] = None
self._on_command: Optional[Callable] = None
self._on_level: Optional[Callable] = None
self._level = 0.0

```
def on_audio_level(self, cb): self._on_level = cb; return self
def on_command(self, cb):     self._on_command = cb; return self
def activate_voice_listening(self):   self._listening = True
def deactivate_voice_listening(self): self._listening = False

def start(self):
    self._running = True
    self._thread = threading.Thread(target=self._loop, daemon=True)
    self._thread.start()
    logger.info("Moteur audio démarré")

def stop(self):
    self._running = False
    if self._thread:
        self._thread.join(timeout=2)

def _loop(self):
    try:
        import sounddevice as sd
        cfg = self.cfg.audio
        voice_buf = []

        def cb(indata, frames, t, status):
            chunk = indata[:, 0]
            level = float(np.sqrt(np.mean(chunk ** 2)))
            self._level = min(1.0, level * 8)
            if self._on_level:
                self._on_level(self._level)
            if not self._listening:
                self.clap.process_chunk(chunk)
            else:
                voice_buf.append(chunk.copy())

        with sd.InputStream(samplerate=cfg.sample_rate, channels=1,
                            blocksize=cfg.chunk_size, dtype='float32', callback=cb):
            logger.info("Microphone ouvert")
            while self._running:
                time.sleep(0.1)
                if self._listening and len(voice_buf) > cfg.sample_rate // cfg.chunk_size * 8:
                    self._process_voice(voice_buf[:])
                    voice_buf.clear()
                    self._listening = False

    except ImportError:
        logger.warning("sounddevice non installé — mode simulation")
        self._simulate()
    except Exception as e:
        logger.error(f"Erreur audio: {e}")
        self._simulate()

def _process_voice(self, buf):
    if not buf or not self.speech: return
    audio = np.concatenate(buf)
    try:
        text = self.speech.transcribe(audio, self.cfg.audio.sample_rate)
        if text and len(text.strip()) > 2 and self._on_command:
            self._on_command(text.strip())
    except Exception as e:
        logger.error(f"STT erreur: {e}")

def _simulate(self):
    import math
    t = 0
    while self._running:
        self._level = (math.sin(t) + 1) / 2 * 0.2
        if self._on_level: self._on_level(self._level)
        t += 0.1
        time.sleep(0.05)
```
