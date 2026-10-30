import json
import os
import subprocess
import time
import urllib.parse
import urllib.request

conversation_history = []


def speak(text):
    """Función de voz nativa de Android."""
    print("Jarvis: " + text)
    clean_text = text.replace("'", "").replace('"', "")
    os.system(f"termux-tts-speak -r 0.85 -p 0.8 '{clean_text}'")


def get_battery_info():
    try:
        out = subprocess.check_output(
            ["termux-battery-status"], stderr=subprocess.DEVNULL
        )
        data = json.loads(out.decode("utf-8"))
        return data.get("percentage", 0), data.get("plugged") != "UNPLUGGED"
    except Exception:
        return None, None


def check_battery_status():
    pct, plugged = get_battery_info()
    if pct is not None:
        state = "conectado" if plugged else "desconectado"
        if pct < 15 and not plugged:
            return f"Atención señor, niveles de energía críticos al {pct} por ciento. Le sugiero conectar el cargador."
        return f"Señor, la batería se encuentra al {pct} por ciento y el sistema de carga está {state}."
    return "No he podido obtener información sobre la batería, señor."


# -------------------------------------------------------------
# CONEXIÓN A INTERNET Y RESUMEN DE NOTICIAS
# -------------------------------------------------------------
def ask_ai_with_internet(prompt_text):
    """Consulta a la IA con búsqueda web activa para datos actualizados."""
    global conversation_history

    system_prompt = (
        "Eres JARVIS. Tienes acceso directo a internet. "
        "Usa información reciente para responder. Sé conciso, elegante, directo y dirígete al usuario como 'señor'."
    )

    history_text = ""
    for turn in conversation_history[-4:]:
        history_text += f"\nUsuario: {turn['user']}\nJARVIS: {turn['bot']}"

    prompt_full = (
        f"{system_prompt}\n{history_text}\nUsuario: {prompt_text}\nJARVIS:"
    )

    try:
        encoded = urllib.parse.quote_plus(prompt_full)
        url = f"https://text.pollinations.ai/{encoded}?model=search"
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            reply = response.read().decode("utf-8").strip()
            if reply:
                conversation_history.append(
                    {"user": prompt_text, "bot": reply}
                )
                return reply
            return "No pude recuperar información de la red en este momento, señor."
    except Exception:
        return (
            "Se presentó un problema al consultar los servidores de red, señor."
        )


def get_news_briefing():
    """Obtiene noticias de las últimas 12 horas desde la red."""
    prompt = (
        "Dame un resumen informativo breve y directo (máximo 3 puntos clave) "
        "con las noticias más relevantes ocurridas en las últimas 12 horas."
    )
    return ask_ai_with_internet(prompt)


# -------------------------------------------------------------
# PROCESAMIENTO DE LENGUAJE NATURAL
# -------------------------------------------------------------
def process_natural_language(text):
    cmd = text.lower()

    if any(k in cmd for k in ["noticias", "novedades", "resumen"]):
        return get_news_briefing()

    elif any(k in cmd for k in ["batería", "bateria", "carga", "energía"]):
        return check_battery_status()

    elif any(k in cmd for k in ["foto", "fotografía", "cámara", "camara"]):
        filename = f"/sdcard/jarvis_{int(time.time())}.jpg"
        os.system(f"termux-camera-photo -c 0 {filename}")
        return "Fotografía capturada y guardada en el almacenamiento, señor."

    elif "volumen" in cmd:
        digits = [int(s) for s in cmd.split() if s.isdigit()]
        if digits:
            val = min(max(digits[0], 0), 15)
            os.system(f"termux-volume call {val}")
            os.system(f"termux-volume music {val}")
            return f"Volumen ajustado al {val}, señor."
        return "Indique un valor numérico entre 0 y 15 para el volumen, señor."

    else:
        return ask_ai_with_internet(text)
