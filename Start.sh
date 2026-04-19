#!/bin/bash
clear
echo “==================================”
echo “   JARVIS - Assistant IA Desktop  “
echo “==================================”
echo “”
echo “Installation des dependances…”
pip3 install fastapi uvicorn sounddevice numpy pyttsx3 httpx psutil websockets
echo “”
echo “Demarrage de JARVIS…”
echo “”
python3 Main.py
