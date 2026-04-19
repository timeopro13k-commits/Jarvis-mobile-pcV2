# Clap_detector.py

import numpy as np
import time
import logging
from typing import Callable, Optional
from dataclasses import dataclass

logger = logging.getLogger(“jarvis.clap”)

@dataclass
class Clap:
timestamp: float
intensity: float

class ClapDetector:
def **init**(self, config):
self.cfg = config
self._history = []
self._noise_floor = 0.01
self._noise_samples = []
self._calibrated = False
self._last_clap = 0.0
self._cooldown_until = 0.0
self._callback: Optional[Callable] = None

```
def on_double_clap(self, cb: Callable):
    self._callback = cb
    return self

def process_chunk(self, chunk: np.ndarray) -> bool:
    if not self._calibrated:
        self._calibrate(chunk)
        return False

    now = time.time()
    if now < self._cooldown_until:
        return False

    rms = self._rms(chunk)
    threshold = self._noise_floor + self.cfg.clap_threshold * 0.5

    if rms > threshold and self._is_transient(chunk):
        if now - self._last_clap < self.cfg.clap_min_interval:
            return False

        self._history.append(Clap(now, min(1.0, rms / (threshold * 3))))
        self._last_clap = now
        self._history = [c for c in self._history if c.timestamp > now - self.cfg.clap_max_interval * 2]

        if len(self._history) >= 2:
            interval = self._history[-1].timestamp - self._history[-2].timestamp
            if self.cfg.clap_min_interval <= interval <= self.cfg.clap_max_interval:
                logger.info("Double clap détecté!")
                self._cooldown_until = now + self.cfg.clap_cooldown
                self._history.clear()
                if self._callback:
                    self._callback()
                return True
    return False

def _rms(self, chunk): return float(np.sqrt(np.mean(chunk.astype(np.float32) ** 2)))

def _calibrate(self, chunk):
    self._noise_samples.append(self._rms(chunk))
    if len(self._noise_samples) >= 88:
        self._noise_floor = np.mean(self._noise_samples) * 1.5
        self._calibrated = True
        logger.info(f"Calibration OK. Noise floor: {self._noise_floor:.4f}")

def _is_transient(self, chunk):
    f = chunk.astype(np.float32)
    q = len(f) // 4
    if q == 0: return True
    r1 = np.sqrt(np.mean(f[:q] ** 2))
    r2 = np.sqrt(np.mean(f[q:] ** 2))
    return (r2 / r1 < 0.8) if r1 > 0.001 else False
```
