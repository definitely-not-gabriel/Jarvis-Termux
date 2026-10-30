
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request


def speak(text):
    """Envía texto al motor TTS de Termux y lo muestra en consola."""
    print("Jarvis: " + text)
    # Sanitizado estricto para evitar fallos en la consola Bash de Termux
    clean_text = text.replace("'", "").replace('"', "")
    os.system(f"termux-tts-speak '{clean_text}'")


def listen():
    """Captura voz desde el micrófono usando la API de Termux."""
    speak("Escuchando sus órdenes, señor...")
    try:
        result = subprocess.check_output(
            ["termux-speech-to-text"], stderr=subprocess.DEVNULL
        )
        command = result.decode("utf-8").strip().lower()
        if command:
            print(f"Usted: {command}")
            return command
        else:
            speak("No logré percibir ninguna orden, señor.")
            return ""
    except Exception:
        print(
            "Jarvis: Error al acceder al micrófono. Verifique que Termux:API"
            " tenga permisos."
        )
        return ""


def get_battery_status():
    """Obtiene el porcentaje y estado de la batería."""
    try:
        out = subprocess.check_output(
            ["termux-battery-status"], stderr=subprocess.DEVNULL
        )
        data = json.loads(out.decode("utf-8"))
        percentage = data.get("percentage", 0)
        plugged = (
            "conectado" if data.get("plugged") != "UNPLUGGED" else "desconectado"
        )
        return f"Señor, la batería se encuentra al {percentage} por ciento y el cargador está {plugged}."
    except Exception:
        return "No pude acceder a la información del sistema de energía, señor."


def adjust_volume(level):
    """Ajusta el volumen del dispositivo (Rango válido: 0 a 15)."""
    try:
        val = int(level)
        if 0 <= val <= 15:
            os.system(f"termux-volume call {val}")
            os.system(f"termux-volume music {val}")
            return f"Nivel de volumen ajustado a {val}, señor."
        else:
            return "Señor, el valor debe estar en un rango de 0 a 15."
    except ValueError:
        return "Señor, debe ingresar un número entero válido."


def take_photo():
    """Toma una fotografía con la cámara trasera y la guarda en el almacenamiento."""
    filename = f"/sdcard/jarvis_photo_{int(time.time())}.jpg"
    try:
        os.system(f"termux-camera-photo -c 0 {filename}")
        return f"Fotografía capturada y guardada en el almacenamiento local, señor."
    except Exception:
        return "No fue posible acceder a la cámara, señor."


def ask_ai(prompt):
    """Realiza consultas a la IA usando una API ligera sin dependencias externas."""
    try:
        system_prompt = (
            "Eres JARVIS, la inteligencia artificial de Iron Man. "
            "Responde de forma muy concisa, elegante, educada y en español, llamando siempre al usuario 'señor'."
        )
        full_prompt = f"{system_prompt}\nUsuario: {prompt}\nJARVIS:"

        # Codificación segura de la URL para evitar errores con caracteres especiales
        encoded_prompt = urllib.parse.quote_plus(full_prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}"

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36"
                )
            },
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            reply = response.read().decode("utf-8").strip()
            if reply:
                return reply
            return "No he recibido una respuesta clara de los servidores, señor."
    except Exception:
        return "Mis servidores de procesamiento no se encuentran disponibles en este momento, señor."


def ai_module():
    """Menú secundario para interacciones avanzadas de IA y control de hardware."""
    speak(
        "Módulo de inteligencia y control activado, señor. ¿Cómo puedo asistirlo?"
    )
    while True:
        print("\n--- MÓDULO JARVIS IA Y CONTROL ---")
        print("1. Comando por Voz")
        print("2. Consulta a la IA")
        print("3. Estado de la Batería")
        print("4. Tomar Fotografía")
        print("5. Ajustar Volumen")
        print("6. Volver al Menú Principal")

        choice = input("Seleccione una opción: ").strip()

        if choice == "1":
            voice_cmd = listen()
            if voice_cmd:
                reply = ask_ai(voice_cmd)
                speak(reply)
        elif choice == "2":
            query = input("Ingrese su consulta para la IA: ").strip()
            if query:
                reply = ask_ai(query)
                speak(reply)
        elif choice == "3":
            speak(get_battery_status())
        elif choice == "4":
            speak(take_photo())
        elif choice == "5":
            vol = input("Ingrese nivel de volumen (0-15): ").strip()
            speak(adjust_volume(vol))
        elif choice == "6":
            speak("Regresando al menú de comandos principales, señor.")
            break


if __name__ == "__main__":
    ai_module()

```
