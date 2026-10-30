
import os
import time
from jarvis_brain import ai_module


def speak(text):
    print("Jarvis: " + text)
    clean_text = text.replace("'", "")
    os.system(f"termux-tts-speak '{clean_text}'")


def main():
    speak(
        "Actualización del sistema completada. Todos los subprocesos están"
        " optimizados y me encuentro listo para su despliegue, señor."
    )
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print(
            "1. Llamar | 2. Siguiente Reel | 3. Auto-Scroll | 4. WhatsApp | 5."
            " IA & Control | 6. Salir"
        )
        query = input(
            "A su disposición, señor. ¿Cuáles son sus órdenes?: "
        ).lower()

        # Realizar llamada
        if query == "1" or "llamar" in query or "call" in query:
            num = input("Número telefónico: ")
            os.system(f"termux-telephony-call {num}")

        # Desplazamiento único
        elif query == "2" or "siguiente" in query or "next" in query:
            os.system("input swipe 500 1500 500 500 200")

        # Desplazamiento automático
        elif query == "3" or "auto" in query:
            speak(
                "Iniciando secuencia de desplazamiento automático, señor. Si"
                " desea abortar el proceso en cualquier momento, presione"
                " Ctrl+C."
            )
            try:
                while True:
                    os.system("input swipe 500 1500 500 500 200")
                    time.sleep(10)
            except KeyboardInterrupt:
                speak(
                    "Señor, he desactivado la función de desplazamiento"
                    " automático. El desplazamiento en pantalla ahora está"
                    " bajo su control manual."
                )

        # Enviar mensaje por WhatsApp
        elif query == "4" or "whatsapp" in query or "mensaje" in query:
            num = input("Número de WhatsApp (con código de país): ")
            msg = input("Mensaje: ")
            speak(
                "Señor, he configurado el protocolo: esto desplegará WhatsApp"
                " directamente en la pantalla de mensajes."
            )
            os.system(
                f"termux-open-url"
                f" 'https://api.whatsapp.com/send?phone={num}&text={msg}'"
            )

        # Módulo JARVIS IA & Control
        elif query == "5" or "ia" in query or "control" in query:
            ai_module()

        # Salir del sistema
        elif query == "6" or "salir" in query or "exit" in query:
            speak("Sistema fuera de línea. Hasta la próxima, señor.")
            break


if __name__ == "__main__":
    main()
