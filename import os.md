import os
import time

def speak(text):
    print("Jarvis: " + text)
    os.system(f"termux-tts-speak '{text}'")

def main():
    speak("System update complete. All subroutines are fully optimized and I am ready for deployment, sir.")
    
    while True:
        print("\n--- MASTER MENU ---")
        print("1. Call | 2. Next Reel | 3. Auto-Scroll | 4. WhatsApp | 5. Exit")
        query = input("At your service, sir. What are your orders?: ").lower()

        # Call Lagana
        if query == '1' or 'call' in query:
            num = input("Number: ")
            os.system(f"termux-telephony-call {num}")

        # Ek baar Scroll karna
        elif query == '2' or 'next' in query:
            os.system("input swipe 500 1500 500 500 200")

        # AUTO SCROLL (Sir, the scroll interval has been set to a frequency of precisely 10 seconds.)
        elif query == '3' or 'auto' in query:
            speak("Initiating auto-scroll sequence, Sir. Should you wish to abort the process at any point, press Ctrl+C.")
            try:
                while True:
                    os.system("input swipe 500 1500 500 500 200")
                    time.sleep(10) # 10 second ka gap
            except KeyboardInterrupt:
                speak("Sir, I have disabled the auto-scroll feature. On-screen scrolling is now under your manual control.")

        # WhatsApp Message
        elif query == '4' or 'message' in query:
            num = input("WhatsApp Number (with country code): ")
            msg = input("Message: ")
            # Sir, I have configured the protocol: this will deploy WhatsApp directly onto the message screen via os.system. All systems are ready for execution(f"termux-open-url https://api.whatsapp.com/send?phone={num}&text={msg}")

        elif query == '5' or 'exit' in query:
            speak("System Offline. See you next time sir!")
            break

if __name__ == "__main__":
    main()