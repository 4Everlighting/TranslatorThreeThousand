#Assignment: Python Project 1
#Joshua Pacheco (JP), 6/04/2023, The Translator Two Thousand, Python3 project
#I am estimating this will take 3 hours to code. It actually took 4 hours to code, as I had issues 
##Spent an additional 1 hour fixing the language output to be the Spanish accent for the when it speaks spanish translation


import sys
import speech_recognition as sr
from textblob import TextBlob
import pyttsx3

#dictionary to define language based on the choice and what to speak as
lang_tr = {
'en': "English",
'es': "Spanish",
}

#function to trabslate the text
def translate_text(text, from_lang, to_lang):
    blob = TextBlob(text)
    translated_text = blob.translate(from_lang=from_lang, to=to_lang)
    return translated_text

#function to speak the text utilizing the pyttsx3 for text to speech functionality
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#Function that utilizes the microphone and listens for speech
def listen_for_speech(language):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print(f"Speak in {lang_tr[language]}...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized {language} Text: {recognized_text}")
        return recognized_text
    except sr.UnknownValueError:
        print("Unable to recognize speech.")
        return None
    except sr.RequestError as e:
        print(f"Recognition request error: {str(e)}")
        return None

#main menu funtion
def menu():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.say("Hello, I am the Translator Interface Three Thousand. Please select from the MENU, but know soon as you you make your selection, and press enter be ready to speak in the language it tells you to speak in.")
    engine.runAndWait()
    while True:
        #print menu to the console for UX
        print("\nTranslation Menu:")
        print("1. English to Spanish Translation")
        print("2. Spanish to English Translation")
        print("3. Exit")
        #for a better user experience, It warns you to be ready to say what you want translated, in the language it needs to be spoke in
        choice = input("Be ready to speak in the language it tells you to speak in!!\nEnter your choice: ")
        #if they choose #1 to have the English to Spanish translation
        if choice == "1":
            english_text = listen_for_speech("en")
            if english_text:
                translated_text = translate_text(english_text, "en", "es")
                print(f"Translated Text: {translated_text}")
                engine.setProperty('voice', voices[2].id)
                speak_text(translated_text)
        #if they choose choice #2 and want Spanish to English translation
        elif choice == "2":
            spanish_text = listen_for_speech("es")
            if spanish_text:
                translated_text = translate_text(spanish_text, "es", "en")
                print(f"Translated Text: {translated_text}")
                engine.setProperty('voice', voices[0].id)
                speak_text(translated_text)
        elif choice == "3":
            sys.exit(0)
        else:
            #error checking for any choices other than 1-3
            print("Invalid choice. Please enter a valid choice.")

if __name__ == "__main__":
    menu()