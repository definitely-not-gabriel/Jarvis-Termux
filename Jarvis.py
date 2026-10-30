from jarvis_brain import (
    check_battery_status,
    get_news_briefing,
    process_natural_language,
    speak,
)


def main():
    speak("Sistemas principales iniciados. Conexión a la red establecida.")

    # 1. Diagnóstico de energía inicial
    pct_msg = check_battery_status()
    if "críticos" in pct_msg:
        speak(pct_msg)

    # 2. Resumen de noticias automático al abrir
    speak(
        "Obteniendo el resumen de noticias de las últimas 12 horas, un"
        " momento..."
    )
    news = get_news_briefing()
    speak(news)

    # 3. Bucle interactivo
    while True:
        try:
            query = input("\n[Señor]: ").strip()
            if not query:
                continue

            if query.lower() in ["salir", "exit", "apagar", "desconectar"]:
                speak("Desactivando sistemas. Hasta pronto, señor.")
                break

            response = process_natural_language(query)
            speak(response)

        except KeyboardInterrupt:
            speak("Secuencia interrumpida. Fuera de línea, señor.")
            break


if __name__ == "__main__":
    main()
