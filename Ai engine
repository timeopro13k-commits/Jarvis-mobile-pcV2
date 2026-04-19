# AI_engine.py

import re
import json
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(“jarvis.ai”)

@dataclass
class Intent:
action: str
target: str = “”
response: str = “”

PATTERNS = [
(r”(?:ouvre|lance|démarre|lancer|start)\s+(.+)”, “launch_app”),
(r”(?:cpu|ram|mémoire|disque|système|infos)”,    “system_info”),
(r”(?:heure|quelle heure|date|quel jour)”,       “get_time”),
(r”(?:bonjour|salut|hello|bonsoir)”,             “greet”),
(r”(?:merci|thanks)”,                            “thanks”),
(r”(?:blague|joke)”,                             “joke”),
(r”(?:aide|help|commandes)”,                     “help”),
(r”(?:au revoir|bye|arrête|stop)”,               “quit”),
(r”(?:calcule|combien)\s+(.+)”,                  “calculate”),
]

JOKES = [
“Pourquoi les robots ne mangent pas ? Parce qu’ils ont déjà un byte.”,
“Comment appelle-t-on un chat dans un pot de peinture ? Un chat-peint.”,
“Pourquoi l’épouvantail a eu un prix ? Il était exceptionnel dans son domaine.”,
]

class AIEngine:
def **init**(self, config):
self.cfg = config.ai
self._joke_i = 0

```
async def process(self, text: str) -> Intent:
    logger.info(f"Commande: '{text}'")

    # Parsing rapide local en premier
    quick = self._quick(text)
    if quick:
        return quick

    # Appel OpenRouter
    result = await self._openrouter(text)
    if result:
        return result

    # Fallback patterns
    return self._patterns(text)

def _quick(self, text: str) -> Optional[Intent]:
    t = text.lower()
    m = re.search(r"(?:ouvre|lance|démarre|lancer|start)\s+(.+)", t)
    if m:
        app = m.group(1).strip()
        return Intent("launch_app", app, f"Je lance {app}.")
    if any(w in t for w in ["heure", "quelle heure", "date"]):
        from datetime import datetime
        now = datetime.now()
        return Intent("speak", "", f"Il est {now.strftime('%H:%M')}, le {now.strftime('%d/%m/%Y')}.")
    return None

async def _openrouter(self, text: str) -> Optional[Intent]:
    try:
        import httpx

        if not self.cfg.api_key or self.cfg.api_key == "VOTRE_CLE_OPENROUTER_ICI":
            logger.warning("Clé OpenRouter non définie, mode patterns activé")
            return None

        system = (
            f"{self.cfg.personality}\n\n"
            "Réponds UNIQUEMENT en JSON :\n"
            '{"action": "launch_app|system_info|speak|quit", '
            '"target": "nom_app_si_applicable", '
            '"response": "ta réponse courte en français"}'
        )

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{self.cfg.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.cfg.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/jarvis-pc",
                    "X-Title": "JARVIS",
                },
                json={
                    "model": self.cfg.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user",   "content": text},
                    ],
                    "max_tokens": self.cfg.max_tokens,
                }
            )

            data = resp.json()
            if "error" in data:
                logger.error(f"OpenRouter: {data['error']}")
                return None

            raw = data["choices"][0]["message"]["content"]
            m = re.search(r'\{.*\}', raw, re.DOTALL)
            if m:
                p = json.loads(m.group())
                return Intent(
                    action=p.get("action", "speak"),
                    target=p.get("target", ""),
                    response=p.get("response", raw),
                )
    except Exception as e:
        logger.error(f"Erreur OpenRouter: {e}")
    return None

def _patterns(self, text: str) -> Intent:
    t = text.lower()
    for pattern, action in PATTERNS:
        m = re.search(pattern, t)
        if m:
            target = m.group(1).strip() if m.lastindex else ""
            return Intent(action, target, self._response(action, target))
    return Intent("speak", "", "Je n'ai pas compris. Dites 'aide' pour la liste des commandes.")

def _response(self, action: str, target: str) -> str:
    from datetime import datetime
    if action == "launch_app":   return f"Je lance {target}."
    if action == "system_info":  return "Je récupère les infos système."
    if action == "get_time":
        now = datetime.now()
        return f"Il est {now.strftime('%H:%M')}, le {now.strftime('%d/%m/%Y')}."
    if action == "greet":
        h = datetime.now().hour
        return f"{'Bonsoir' if h >= 18 else 'Bonjour'}. Que puis-je faire pour vous ?"
    if action == "thanks":       return "Avec plaisir."
    if action == "joke":
        j = JOKES[self._joke_i % len(JOKES)]; self._joke_i += 1; return j
    if action == "help":
        return "Je peux lancer des apps, donner l'heure, les infos système, faire des calculs et raconter des blagues."
    if action == "quit":         return "À bientôt."
    if action == "calculate":    return self._calc(target)
    return "Commande reçue."

def _calc(self, expr: str) -> str:
    try:
        e = expr
        e = re.sub(r'\bplus\b', '+', e)
        e = re.sub(r'\bmoins\b', '-', e)
        e = re.sub(r'\bfois\b|\bmultiplié par\b', '*', e)
        e = re.sub(r'\bdivisé par\b', '/', e)
        clean = re.sub(r'[^0-9+\-*/().\s]', '', e).strip()
        if not clean: return "Je n'ai pas pu interpréter ce calcul."
        return f"Le résultat est {round(eval(clean, {'__builtins__': {}}, {}), 4)}."
    except:
        return "Je n'ai pas pu effectuer ce calcul."
```
