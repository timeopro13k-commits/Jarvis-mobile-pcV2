# Commander.py

import asyncio
import platform
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(“jarvis.cmd”)

APPS = {
“darwin”: {
“chrome”: “open -a ‘Google Chrome’”, “firefox”: “open -a Firefox”,
“safari”: “open -a Safari”, “code”: “open -a ‘Visual Studio Code’”,
“vscode”: “open -a ‘Visual Studio Code’”, “terminal”: “open -a Terminal”,
“finder”: “open -a Finder”, “spotify”: “open -a Spotify”,
“calculator”: “open -a Calculator”, “notes”: “open -a Notes”,
},
“linux”: {
“chrome”: “google-chrome”, “firefox”: “firefox”, “code”: “code”,
“vscode”: “code”, “terminal”: “x-terminal-emulator”,
“files”: “nautilus”, “spotify”: “spotify”, “calculator”: “gnome-calculator”,
},
“windows”: {
“chrome”: “start chrome”, “firefox”: “start firefox”, “code”: “start code”,
“vscode”: “start code”, “terminal”: “start cmd”, “files”: “explorer”,
“notepad”: “start notepad”, “calculator”: “start calc”,
}
}

class Result:
def **init**(self, ok: bool, out: str = “”, err: str = “”):
self.success = ok; self.output = out; self.error = err

class Commander:
def **init**(self, config):
self.cfg = config.security
self.os = platform.system().lower()

```
async def launch_app(self, name: str) -> Result:
    n = name.lower().strip()
    if n not in [a.lower() for a in self.cfg.allowed_apps]:
        return Result(False, err=f"'{name}' non autorisé.")

    cmd = APPS.get(self.os, {}).get(n)
    if not cmd:
        if shutil.which(n): cmd = n
        else: return Result(False, err=f"'{name}' introuvable.")

    logger.info(f"Lance: {cmd}")
    return await self._run(cmd)

async def get_system_info(self) -> dict:
    try:
        import psutil
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory": {"percent": psutil.virtual_memory().percent},
            "disk": {"percent": psutil.disk_usage('/').percent},
            "platform": platform.system(),
        }
    except: return {}

async def open_file(self, path: str) -> Result:
    p = Path(path)
    if not p.exists(): return Result(False, err="Fichier introuvable.")
    try: p.relative_to(Path.home())
    except: return Result(False, err="Accès refusé.")
    cmds = {"darwin": f"open '{path}'", "linux": f"xdg-open '{path}'", "windows": f"start '' '{path}'"}
    return await self._run(cmds.get(self.os, f"open '{path}'"))

async def _run(self, cmd: str, timeout: int = 10) -> Result:
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await asyncio.wait_for(proc.communicate(), timeout)
        return Result(proc.returncode == 0, out.decode(errors='ignore'), err.decode(errors='ignore'))
    except asyncio.TimeoutError: return Result(False, err="Timeout")
    except Exception as e: return Result(False, err=str(e))
```
